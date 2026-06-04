Copyright © Charles Roux 2026

# Codebase Integrity & System Validation Report

**Date:** 2026-03-01  
**Scope:** Kyosan Consciousness Framework — app, API, persistence, frontend.

---

## 1. Architecture Overview

| Layer | Component | Role |
|-------|-----------|------|
| **Web** | Flask + Flask-SocketIO + CORS | App entry, routes, WebSocket |
| **API** | `app/routes.py` | REST + Socket.IO handlers |
| **Consciousness** | `AdvancedConsciousnessInterface` | Units, 7 principles, persistence |
| **Framework** | `consciousness_framework.py` | ConsciousnessSystem, SelfModelingUnit |
| **LLM** | `ModelInterface` (OpenRouter) | Chat completions, parameter validation |
| **Frontend** | `app/templates/index.html` + `app/static/js/app.js` + CSS | UI, parameters, units, history |

---

## 2. API Routes — Verified

| Method | Endpoint | Handler | Backend method | Status |
|--------|----------|---------|----------------|--------|
| GET | `/` | index | render index.html | ✅ |
| GET | `/api/units` | get_units | get_all_units() | ✅ |
| POST | `/api/units` | create_unit | create_unit(unit_id) | ✅ |
| DELETE | `/api/units/<id>` | delete_unit | delete_unit(unit_id) | ✅ |
| GET | `/api/units/<id>/state` | get_unit_state | get_unit_state(unit_id) | ✅ |
| POST | `/api/units/<id>/process` | process_input | process_input() + model_interface | ✅ |
| POST | `/api/units/<id>/feedback` | apply_feedback | apply_user_feedback() | ✅ |
| GET | `/api/history` | get_history | get_processing_history() | ✅ |
| GET | `/api/conversations` | get_conversations | get_conversation_history() | ✅ |
| GET/POST | `/api/sessions` | sessions | get_all_sessions(), create_new_session() | ✅ |
| DELETE | `/api/sessions/<id>` | delete_session | delete_session() | ✅ |
| POST | `/api/export` | export_data | export_data() | ✅ |
| GET | `/api/storage/stats` | get_storage_stats | (inline) | ✅ |
| POST | `/api/test/model` | test_model | model_interface.process_with_model | ✅ |
| POST | `/api/test/consciousness` | test_consciousness | process_input + model | ✅ |
| Socket.IO | connect / disconnect / process_input | handle_connect, etc. | consciousness_interface.process_input | ✅ |

All route handlers exist and call the correct backend methods.

---

## 3. Backend Integration

### 3.1 AdvancedConsciousnessInterface (`app/advanced_consciousness_interface.py`)

- **Persistence:** Loads/saves `consciousness_states`, `conversations`, `processing_history`, `session_logs` under `consciousness_data/`.
- **Startup:** `_load_persistent_data()` then `_restore_units_from_persistent_data()` so saved units and conversations are restored after restart.
- **Units:** Create unit → persisted in `consciousness_states` + `_save_persistent_data()`. Delete unit → removed from `consciousness_states` and `conversations` and saved.
- **State serialization:** `_serialize_consciousness_state()` used for get_all_units, get_unit_state, create_unit response (JSON-safe, no non-serializable metrics).
- **Methods used by routes:** get_all_units, create_unit, delete_unit, get_unit_state, process_input, get_processing_history, get_conversation_history, get_all_sessions, create_new_session, delete_session, export_data, save_conversation, apply_user_feedback — all implemented and wired.

### 3.2 ModelInterface (`app/model_interface.py`)

- **Config:** Reads `OPENROUTER_API_KEY`, `OPENROUTER_API_BASE`, `OPENROUTER_MODEL` from env (`.env` via `load_dotenv()`).
- **Parameters:** `_validate_parameters()` clamps all 14 parameters to valid ranges; only validated params are sent to OpenRouter.
- **API call:** `process_with_model()` builds messages, calls `client.chat.completions.create()` with temperature, max_tokens, top_p, presence_penalty, frequency_penalty.

### 3.3 Consciousness Framework (`consciousness_framework.py`)

- **ConsciousnessSystem:** create_unit(), units dict.
- **SelfModelingUnit:** process(), get_consciousness_state(), learn(), memory, etc.
- **Used by:** AdvancedConsciousnessInterface only (not the legacy `consciousness_interface.py` for main flow).

### 3.4 Fix applied during validation

- **Feedback response key:** Routes expected `result['unit_state']` after `apply_user_feedback()`; the interface returns `result['state']`. Routes updated to use `result.get('unit_state') or result.get('state')` for the Socket.IO unit update so the frontend still receives updates after feedback.

---

## 4. Frontend ↔ API Contract

| Frontend action | API call | Expected response | Status |
|-----------------|----------|-------------------|--------|
| Load units | GET /api/units | `{ status, units }` | ✅ |
| Create unit | POST /api/units `{ unit_id }` | `{ status, message, unit? }` | ✅ |
| Delete unit | DELETE /api/units/:id | 200 + body | ✅ |
| Select unit | GET /api/units/:id/state, GET /api/history?unit_id= | state + history | ✅ |
| Process input | POST /api/units/:id/process `{ input, parameters }` | `{ status, response, state, ... }` | ✅ |
| Follow-up | Same with conversation_context / is_follow_up | Same shape | ✅ |
| Feedback | POST /api/units/:id/feedback `{ feedback_type, intensity }` | `{ status, ... }` | ✅ |
| Conversations | GET /api/conversations?unit_id= | `{ status, conversations }` | ✅ |
| Sessions | GET/POST /api/sessions, DELETE /api/sessions/:id | sessions list / create / delete | ✅ |
| Export / Storage stats | POST /api/export, GET /api/storage/stats | paths / stats | ✅ |

Frontend uses these endpoints and response shapes consistently (including `getCurrentParameters()` and parameter validation).

---

## 5. Persistence Integrity

| Store | File | Load | Save | Used for |
|-------|------|------|------|----------|
| consciousness_states | consciousness_data/consciousness_states.json | ✅ _load_persistent_data | ✅ _save_persistent_data | Unit list, restore state on startup |
| conversations | consciousness_data/conversations.json | ✅ | ✅ _save_conversation → _save_persistent_data | Per-unit conversation history |
| processing_history | consciousness_data/processing_history.json | ✅ | ✅ (written in _save_persistent_data) | Processing history per unit |
| session_logs | consciousness_data/session_logs.json | ✅ | ✅ _log_session_event → _save_persistent_data | Session events |

- **Restore on startup:** `_restore_units_from_persistent_data()` builds the set of unit IDs from `consciousness_states` and `conversations`, creates each missing unit in `system.units`, and restores consciousness state from `consciousness_states` when present.
- **Create unit:** New unit is written to `consciousness_states` and `_save_persistent_data()` is called so it survives restart.
- **Delete unit:** Unit is removed from `system.units`, `consciousness_states`, `conversations`, `processing_history`, and `_save_persistent_data()` is called.

---

## 6. Configuration & Environment

| Variable | Purpose | Default / note |
|----------|---------|-----------------|
| OPENROUTER_API_KEY | LLM API key | Required for process |
| OPENROUTER_API_BASE | OpenRouter base URL | https://openrouter.ai/api/v1 |
| OPENROUTER_MODEL | Model id | e.g. qwen/qwen3.5-plus-02-15 |
| SITE_URL | HTTP-Referer for OpenRouter | Optional |
| SITE_NAME | X-Title for OpenRouter | Optional |
| SECRET_KEY | Flask secret | From .env |
| FLASK_ENV | Environment | development etc. |

`.env` is loaded via `load_dotenv()` in app and in `model_interface.py`. No API key is hardcoded in the main app path.

---

## 7. Systems Active and Implemented

| System | Implemented | Notes |
|--------|-------------|--------|
| Unit CRUD | ✅ | Create, list, delete, get state; persisted and restored |
| Process input (7 principles) | ✅ | Preprocess, full integration, model call, save conversation |
| LLM integration (OpenRouter) | ✅ | Env-based config, parameter validation, chat completions |
| Conversation persistence | ✅ | Per unit, per session, saved to conversations.json |
| Session management | ✅ | get_all_sessions, create_new_session, delete_session |
| Processing history | ✅ | Per unit, loaded/saved, returned by /api/history |
| Feedback (excellent/positive/neutral/poor) | ✅ | apply_user_feedback, state saved, Socket.IO unit update |
| Export / Storage stats | ✅ | export_data, get_storage_stats |
| Parameter panel (14 params + info) | ✅ | Validated backend; frontend getNum/getInt; “i” descriptions |
| Real-time updates | ✅ | Socket.IO unit_update on process and feedback |
| New unit modal & default unit dropdown | ✅ | Modal top-level; dropdown only updated on success |

---

## 8. Run-Time Check

- Imports: `from app import app, socketio` and `AdvancedConsciousnessInterface`, `model_interface` — **OK**.
- `AdvancedConsciousnessInterface()` loads persistent data and restores units from disk — **OK**.
- `get_all_units()` returns a `units` dict — **OK**.
- `model_interface.process_with_model` is available — **OK**.

---

## 9. Summary

- **Integrity:** All route handlers, backend methods, and persistence paths are present and wired correctly. One fix was applied: feedback route now uses `result.get('unit_state') or result.get('state')` for Socket.IO.
- **Systems:** Unit lifecycle, process input with 7 principles, LLM (OpenRouter), conversations, sessions, history, feedback, export, and storage stats are implemented and active.
- **Persistence:** Units and conversations are saved and restored across restarts; create/delete unit update disk consistently.
- **Config:** API key and model are read from `.env`; parameters are validated and clamped before use.

No remaining gaps or known broken flows were found for the main app and API.

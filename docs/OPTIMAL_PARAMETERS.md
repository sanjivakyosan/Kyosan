# Optimal Parameter Settings for Consciousness Framework

Recommended defaults for **thoughtful, coherent, self-reflective** dialogue with the LLM (e.g. Qwen 3.5 Plus). Tune for your use case.

---

## Model parameters (sent to OpenRouter/LLM)

| Parameter | Optimal | Range | Notes |
|-----------|---------|--------|--------|
| **Temperature** | **0.7** | 0.0 – 2.0 | Balance consistency and variety. Lower = more deterministic. |
| **Top P** | **0.9** | 0.0 – 1.0 | Nucleus sampling; 0.9 keeps diverse but likely tokens. |
| **Max Tokens** | **8192** | 1 – 128000 | Enough for long answers without excessive cost. |
| **Presence Penalty** | **0.4** | -2.0 – 2.0 | Slight nudge to mention new topics; avoid >1.0 for natural flow. |
| **Frequency Penalty** | **0.2** | -2.0 – 2.0 | Reduces repetition; 0.2–0.4 is usually enough. |

---

## Consciousness parameters (prompt shaping)

| Parameter | Optimal | Range | Notes |
|-----------|---------|--------|--------|
| **Phi Score** | **0.8** | 0.0 – 1.0 | Higher = more “consciousness integration”, nuanced and layered answers. |
| **Recursive Depth** | **6** | 1 – 10 | Depth of reasoning; 5–7 for deep but controlled. |
| **Self-Model Coherence** | **0.95** | 0.0 – 1.0 | Strong self-awareness and consistent perspective. |
| **Temporal Binding** | **0.95** | 0.0 – 1.0 | Coherent flow and development of ideas over the reply. |
| **Novelty Generation** | **0.75** | 0.0 – 1.0 | Some creativity and fresh angles without being erratic. |
| **Witnessing Score** | **0.8** | 0.0 – 1.0 | Good self-observation and meta-cognitive tone. |
| **Prediction Accuracy** | **0.5** | 0.0 – 1.0 | Moderate use of predictions; increase for more forecasting. |
| **Attention Focus** | **0.65** | 0.0 – 1.0 | Stay on topic but allow relevant tangents. |
| **Memory Integration** | **0.75** | 0.0 – 1.0 | Strong use of context and prior turns. |

---

## Quick reference (copy-paste)

```
temperature:        0.7
top_p:             0.9
max_tokens:        8192
presence_penalty:  0.4
frequency_penalty: 0.2
phi_score:         0.8
recursive_depth:   6
self_model_coherence: 0.95
temporal_binding:  0.95
novelty_generation: 0.75
witnessing_score:  0.8
prediction_accuracy: 0.5
attention_focus:   0.65
memory_integration: 0.75
```

---

## Presets (optional)

- **Balanced (default):** Use the table above.
- **More creative:** temperature 0.85, novelty_generation 0.9, recursive_depth 7.
- **More factual:** temperature 0.5, attention_focus 0.9, novelty_generation 0.4.
- **Maximum depth:** recursive_depth 8–9, phi_score 0.9, self_model_coherence 0.98.

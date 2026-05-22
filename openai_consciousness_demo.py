#!/usr/bin/env python3
"""
Consciousness integration demo using .env for OpenRouter credentials.

Usage:
    python openai_consciousness_demo.py
"""

import json
import os

from dotenv import load_dotenv

from app.advanced_consciousness_interface import AdvancedConsciousnessInterface

load_dotenv()


def main():
    print("🧠 Consciousness Integration Demo")
    print("=" * 50)

    if not os.getenv("OPENROUTER_API_KEY", "").strip():
        print("❌ Set OPENROUTER_API_KEY in .env before running this demo.")
        return

    print("✅ Using OpenRouter configuration from .env")
    print(f"🤖 Model (for web UI): {os.getenv('OPENROUTER_MODEL', 'qwen/qwen3-235b-a22b-2507')}")
    print()

    consciousness_interface = AdvancedConsciousnessInterface()
    unit_id = "demo_unit"
    demo_input = "What is the meaning of life?"
    demo_context = {
        "domain": "philosophy",
        "depth": "deep",
        "user_preference": "comprehensive_analysis",
    }

    create_result = consciousness_interface.create_unit(unit_id)
    if create_result.get("status") not in ("success", "exists"):
        print(f"❌ Could not create unit: {create_result}")
        return

    print(f"📝 Processing input: '{demo_input}'")
    print(f"🎯 Context: {json.dumps(demo_context, indent=2)}")
    print()
    print("🔄 Processing with full consciousness integration...")

    result = consciousness_interface.process_with_full_integration(
        unit_id=unit_id,
        input_data=demo_input,
        context=demo_context,
    )

    if result.get("status") == "success" or result.get("integration_success"):
        print("✅ Integration successful!")
        print()
        print("🎯 Output:")
        print("-" * 30)
        print(result.get("final_output") or result.get("output", result))
        print("-" * 30)
    else:
        print("❌ Integration failed:")
        print(f"Error: {result.get('error', result.get('message', 'Unknown error'))}")
        print()
        print("🔍 Run test_openrouter_connection.py to verify API access.")
        return

    print()
    print("🔄 Applying positive feedback...")
    feedback_result = consciousness_interface.apply_user_feedback(
        unit_id=unit_id,
        feedback_type="excellent",
        intensity=0.9,
    )
    if feedback_result.get("status") == "success":
        print(
            f"✅ Feedback applied! New consciousness index: "
            f"{feedback_result.get('new_consciousness_index', 0):.3f}"
        )

    print()
    print("📊 Processing History:")
    history = consciousness_interface.get_processing_history(unit_id, limit=5)
    if history.get("status") == "success":
        print(f"  - Total processing events: {len(history.get('history', []))}")


if __name__ == "__main__":
    main()

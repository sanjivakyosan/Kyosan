#!/usr/bin/env python3
"""Test OpenRouter model configured in .env."""

import os
import time

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def _client():
    api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("Set OPENROUTER_API_KEY in .env")
    return OpenAI(
        base_url=os.getenv("OPENROUTER_API_BASE", "https://openrouter.ai/api/v1").strip(),
        api_key=api_key,
    )


def test_kimi_model():
    model = os.getenv("OPENROUTER_MODEL", "qwen/qwen3-235b-a22b-2507").strip()
    site_url = os.getenv("SITE_URL", "http://localhost:5001").strip()
    site_name = os.getenv("SITE_NAME", "Consciousness Framework").strip()

    print("🔗 Testing OpenRouter model from .env")
    print("=" * 60)
    client = _client()

    try:
        print("📡 Connecting to OpenRouter...")
        print(f"   Model: {model}")
        print()
        print("🚀 Making API request...")
        start_time = time.time()

        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": site_url,
                "X-Title": site_name,
            },
            model=model,
            messages=[{"role": "user", "content": "What is the meaning of life?"}],
        )

        response_time = time.time() - start_time
        print("✅ API call successful!")
        print(f"⏱️  Response time: {response_time:.2f} seconds")
        print()
        print("🤖 Response:")
        print("-" * 40)
        print(completion.choices[0].message.content)
        print("-" * 40)
        print(f"   Model: {completion.model}")
        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    success = test_kimi_model()
    print("\n✅ Test completed successfully!" if success else "\n❌ Test failed!")

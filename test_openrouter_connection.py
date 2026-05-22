#!/usr/bin/env python3
"""OpenRouter API connection test using .env configuration."""

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


def test_openrouter_connection():
    model = os.getenv("OPENROUTER_MODEL", "qwen/qwen3-235b-a22b-2507").strip()
    site_url = os.getenv("SITE_URL", "http://localhost:5001").strip()
    site_name = os.getenv("SITE_NAME", "Consciousness Framework").strip()

    print("🔗 Testing OpenRouter API Connection")
    print("=" * 50)
    client = _client()

    try:
        print(f"   Model: {model}")
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
        print("🤖 AI Response:")
        print("-" * 30)
        print(completion.choices[0].message.content)
        print("-" * 30)
        print(f"   Model: {completion.model}")
        return True

    except Exception as e:
        print(f"❌ API call failed: {e}")
        return False


def test_alternative_models():
    print("🔄 Testing alternative models...")
    client = _client()
    site_url = os.getenv("SITE_URL", "http://localhost:5001").strip()
    site_name = os.getenv("SITE_NAME", "Consciousness Framework").strip()

    models_to_try = [
        "meta-llama/llama-3.2-3b-instruct:free",
        "microsoft/phi-3-mini-128k-instruct:free",
        "google/gemma-2-9b-it:free",
    ]

    for model in models_to_try:
        try:
            print(f"🧪 Testing model: {model}")
            completion = client.chat.completions.create(
                extra_headers={"HTTP-Referer": site_url, "X-Title": site_name},
                model=model,
                messages=[{"role": "user", "content": "Hello, are you working?"}],
                max_tokens=50,
            )
            if completion.choices:
                print(f"✅ {model} - Working!")
                return model
        except Exception as e:
            print(f"❌ {model} - Failed: {e}")

    return None


if __name__ == "__main__":
    print("🧠 OpenRouter API Connection Test\n")
    success = test_openrouter_connection()
    if not success:
        print("🔄 Main model failed, trying alternatives...")
        alternative_model = test_alternative_models()
        if alternative_model:
            print(f"💡 Suggestion: set OPENROUTER_MODEL={alternative_model} in .env")

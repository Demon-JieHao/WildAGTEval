"""
Test script for LiteLLM unified API using Claude (Anthropic) model.
Run this after setting your Anthropic API key:
    export ANTHROPIC_API_KEY="sk-ant-..."
"""

from API_Complexity.utils.litellm_api import call_litellm_api

def main():
    print("🚀 Testing Claude model via LiteLLM unified API...\n")

    prompt = "Write a short haiku about the beauty of code."
    # model = "anthropic/claude-3-7-sonnet-20250219"
    # Try multiple fallback models to verify Anthropic connectivity
    test_models = [
        "claude-sonnet-4-20250514"
    ]

    for model in test_models:
        print(f"\n🔍 Testing model: {model}")
        response = call_litellm_api(
            prompt=prompt,
            model=model,
            model_name="claude",
            thinking=False
        )
        print("✅ Model:", model)
        print("💬 Response:\n", response)
    return



if __name__ == "__main__":
    main()

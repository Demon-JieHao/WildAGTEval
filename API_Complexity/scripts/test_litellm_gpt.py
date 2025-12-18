"""
Test script for LiteLLM unified API using GPT model.
Run this after setting your OpenAI API key:
    export OPENAI_API_KEY="sk-..."
"""

from API_Complexity.utils.litellm_api import call_litellm_api

def main():
    print("🚀 Testing GPT model via LiteLLM unified API...\n")

    prompt = "Explain shortly about Amazon"
    model = "gpt-4o-mini"

    response = call_litellm_api(
        prompt=prompt,
        model=model,
        model_name="gpt",
        thinking=False
    )

    print("✅ Model:", model)
    print("🧠 Prompt:", prompt)
    print("\n💬 Response:\n", response)


if __name__ == "__main__":
    main()

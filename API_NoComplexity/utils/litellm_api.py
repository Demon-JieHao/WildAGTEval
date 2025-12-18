"""
Unified LLM API integration using LiteLLM.
Supports Claude (Anthropic), GPT (OpenAI), and other providers.
Maintains compatibility with previous claude_api.py parameters.
"""

import os
import json
import re
import time
import random
from typing import Optional, Dict, Any, List
from litellm import completion
from freezegun import freeze_time
import litellm

def initialize_litellm_client():
    """Initialize LiteLLM environment (no explicit client needed)."""
    print("✅ LiteLLM initialized. Available providers: OpenAI, Anthropic, Mistral, etc.")
    return completion

def call_litellm_api(
    claude_client=None,
    prompt: str = "",
    model_name: str = "claude",
    model: str = "anthropic/claude-3-7-sonnet-20250219",
    max_retries: int = 5,
    base_delay: float = 0.5,
    thinking: bool = False,
):
    """
    Unified API call supporting Claude, GPT, and others.
    Maintains compatibility with call_claude_api() signature.
    """
    if not prompt:
        print("Error: Empty prompt provided.")
        return "ERROR: Empty prompt"

    for attempt in range(max_retries + 1):
        try:
            kwargs = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 10000,
                "stop": ["<API_RESPONSE>", "<USER_QUERY>", "H:"],
            }

            # Anthropic-specific thinking mode
            if thinking and ("claude" in model.lower() or "anthropic" in model.lower()):
                kwargs["thinking"] = {"type": "enabled", "budget_tokens": 2000}
                kwargs["temperature"] = 1  # required for thinking mode
            else:
                kwargs["temperature"] = 0  # deterministic for non-thinking mode

            
            response = completion(**kwargs)
            return response["choices"][0]["message"]["content"]

        except Exception as e:
            error_str = str(e)
            is_rate_limit_error = (
                "429" in error_str
                or "rate limit" in error_str.lower()
                or "throttle" in error_str.lower()
            )

            if is_rate_limit_error and attempt < max_retries:
                delay = base_delay * (2 ** attempt)
                jitter = random.uniform(0.1, 0.3) * delay
                total_delay = delay + jitter
                print(f"⚠️ Rate limit hit. Retrying in {total_delay:.1f}s... (attempt {attempt + 1}/{max_retries})")
                time.sleep(total_delay)
                continue

            print(f"❌ Error calling model {model}: {e}")
            return f"ERROR: {error_str}"

    return "ERROR: Max retries exceeded"


def extract_json_from_response(text: str) -> str:
    """Extract JSON array or object from model response text."""
    json_match = re.search(r"\[\s*{.*}\s*\]", text, re.DOTALL)
    if json_match:
        return json_match.group(0)

    json_match = re.search(r"{\s*\".*}\s*", text, re.DOTALL)
    if json_match:
        return json_match.group(0)

    return text


def validate_litellm_response(response_text: str) -> List[Dict]:
    """
    Extract and validate JSON from model response.
    Returns list of valid trail dictionaries or empty list if parsing fails.
    """
    if response_text.startswith("ERROR:"):
        print(f"LLM API error: {response_text}")
        return []

    try:
        json_str = extract_json_from_response(response_text)
        trails = json.loads(json_str)

        if not isinstance(trails, list):
            if isinstance(trails, dict):
                return [trails]
            print(f"Warning: Expected a list of trails, got {type(trails)}")
            return []

        valid_trails = []
        for trail in trails:
            if all(key in trail for key in ["name", "description", "user", "api_calls"]):
                valid_trails.append(trail)
            else:
                print(f"Warning: Trail missing required fields: {trail.get('name', 'unnamed')}")

        return valid_trails
    except json.JSONDecodeError as e:
        print(f"Error parsing LLM response as JSON: {e}")
        print("Response was:", response_text[:200], "..." if len(response_text) > 200 else "")
        return []
    except Exception as e:
        print(f"Unexpected error validating LLM response: {e}")
        return []

"""
OpenAI API integration utilities for benchmark generation.
Supports OpenAI-compatible APIs like vLLM, Ollama, and local servers.
"""

import os
import json
import time
import random
from typing import Optional, Dict, Any, List
from openai import OpenAI


def initialize_openai_client(base_url: str = "http://127.0.0.1:8000/v1", 
                           api_key: str = None, 
                           timeout: float = 30.0):
    """Initialize and return the OpenAI API client.
    
    Args:
        base_url: API endpoint URL (default: OpenAI API)
        api_key: API key (if None, will try environment variable)
        timeout: Request timeout in seconds
        
    Returns:
        OpenAI client instance or None if initialization fails
    """
    try:
        # Get API key from parameter or environment
        if api_key is None:
            api_key = os.environ.get('OPENAI_API_KEY', 'token-abc123')
        
        # Initialize the client
        client = OpenAI(
            base_url=base_url,
            api_key=api_key,
            timeout=timeout
        )
        
        return client
    except Exception as e:
        print(f"Error initializing OpenAI client: {e}")
        return None


def call_openai_api(client, prompt: str, 
                   model: str = "Qwen/Qwen3-32B",
                   max_retries: int = 50,
                   base_delay: float = 1.0,
                   temperature: float = 0.0,
                   max_tokens: int = 4096,
                   thinking: bool = False):
    """Call the OpenAI API with the given prompt, with retry logic for rate limiting.
    
    Args:
        client: Initialized OpenAI client
        prompt: The prompt to send to the model
        model: Model to use (e.g., "gpt-3.5-turbo", "Qwen/Qwen3-32B")
        max_retries: Maximum number of retry attempts for rate limiting
        base_delay: Base delay in seconds for exponential backoff
        temperature: Sampling temperature
        max_tokens: Maximum tokens in response
        thinking: Whether to enable thinking mode (not supported in OpenAI API)
        
    Returns:
        Model's response text or error message
    """
    if not client:
        print("Error: OpenAI client not initialized.")
        return "ERROR: API client not available"
    
    # Convert single prompt to messages format
    messages = [{"role": "user", "content": prompt}]
    
    # Stop sequences to match Claude API behavior
    stop_sequences = ['<API_RESPONSE>', '<USER_QUERY>', 'H:']
    
    for attempt in range(max_retries + 1):
        time.sleep(0.5)
        try:
            # Make the API call
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stop=stop_sequences
            )
            
            # Extract the response text
            if response.choices and len(response.choices) > 0:
                return response.choices[0].message.content
            else:
                return "ERROR: No response from model"
                
        except Exception as e:
            error_str = str(e)
            
            # Check if this is a retryable error
            is_retryable_error = (
                "429" in error_str or 
                "rate limit" in error_str.lower() or
                "throttle" in error_str.lower() or
                "too many requests" in error_str.lower() or
                "404" in error_str or
                "does not exist" in error_str.lower() or
                "NotFoundError" in error_str
            )
            
            # If it's a retryable error and we have retries left, wait and retry
            if is_retryable_error and attempt < max_retries:
                # Calculate delay with exponential backoff and jitter
                delay = base_delay * (3 * attempt)
                jitter = random.uniform(0.1, 0.3) * delay  # Add 10-30% jitter
                total_delay = delay + jitter
                
                # Determine error type for logging
                if "404" in error_str or "does not exist" in error_str.lower():
                    print(f"⚠️  Model not found. Retrying in {total_delay:.1f}s... (attempt {attempt + 1}/{max_retries})")
                else:
                    print(f"⚠️  Rate limit hit. Retrying in {total_delay:.1f}s... (attempt {attempt + 1}/{max_retries})")
                time.sleep(total_delay)
                continue
            
            # Either not a retryable error, or we've exhausted retries
            if is_retryable_error:
                print(f"❌ Retryable error persisted after {max_retries} retries: {error_str}")
            else:
                print(f"Error calling OpenAI API: {e}")
            
            return f"ERROR: {error_str}"


def extract_json_from_response(text: str) -> str:
    """Extract JSON array from model's response text."""
    import re
    
    # Look for array pattern starting with [ and ending with ]
    json_match = re.search(r'\[\s*{.*}\s*\]', text, re.DOTALL)
    if json_match:
        return json_match.group(0)
    
    # If not found, look for object pattern
    json_match = re.search(r'{\s*".*}\s*', text, re.DOTALL)
    if json_match:
        return json_match.group(0)
    
    # If we can't find any JSON pattern, return the whole text
    return text


def validate_openai_response(response_text: str) -> List[Dict]:
    """
    Extract and validate JSON from OpenAI model's response.
    
    Returns:
        List of valid trail dictionaries or empty list if parsing fails
    """
    if response_text.startswith("ERROR:"):
        print(f"OpenAI API error: {response_text}")
        return []
    
    try:
        # Extract JSON content
        json_str = extract_json_from_response(response_text)
        
        # Parse the JSON
        trails = json.loads(json_str)
        
        # Ensure it's a list
        if not isinstance(trails, list):
            if isinstance(trails, dict):
                # Single trail returned as dict
                return [trails]
            print(f"Warning: Expected a list of trails, got {type(trails)}")
            return []
        
        # Check each trail has required fields
        valid_trails = []
        for trail in trails:
            if all(key in trail for key in ["name", "description", "user", "api_calls"]):
                valid_trails.append(trail)
            else:
                print(f"Warning: Trail missing required fields: {trail.get('name', 'unnamed')}")
        
        return valid_trails
    except json.JSONDecodeError as e:
        print(f"Error parsing OpenAI response as JSON: {e}")
        print("Response was:", response_text[:200], "..." if len(response_text) > 200 else "")
        return []
    except Exception as e:
        print(f"Unexpected error validating OpenAI response: {e}")
        return []


def test_openai_connection(base_url: str = "http://127.0.0.1:8000/v1", 
                          model: str = "Qwen/Qwen3-32B",
                          api_key: str = "token-abc123"):
    """Test OpenAI API connection with a simple request.
    
    Args:
        base_url: API endpoint URL
        model: Model name to test
        api_key: API key for authentication
        
    Returns:
        True if connection successful, False otherwise
    """
    try:
        print(f"Testing OpenAI API connection...")
        print(f"  Base URL: {base_url}")
        print(f"  Model: {model}")
        
        client = initialize_openai_client(base_url=base_url, api_key=api_key)
        if not client:
            print("  ❌ Failed to initialize client")
            return False
        
        response = call_openai_api(
            client=client,
            prompt="Hello! Please respond with 'API connection successful.'",
            model=model,
            max_retries=10  # More retries for testing to handle model loading issues
        )
        
        if response.startswith("ERROR:"):
            print(f"  ❌ API call failed: {response}")
            return False
        
        print(f"  ✅ API call successful")
        print(f"  Response: {response[:100]}...")
        return True
        
    except Exception as e:
        print(f"  ❌ Connection test failed: {e}")
        return False


if __name__ == "__main__":
    # Test with local vLLM server (matching openai_test.py)
    test_openai_connection(
        base_url="http://127.0.0.1:8000/v1",
        model="Qwen/Qwen3-32B",
        api_key="token-abc123"
    )

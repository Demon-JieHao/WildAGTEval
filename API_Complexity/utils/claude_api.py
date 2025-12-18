"""
Claude API integration utilities for benchmark generation.
"""

import os
import json
import re
import time
import random
from typing import Optional, Dict, Any, List
from anthropic import AnthropicBedrock
import boto3
from freezegun import freeze_time



def initialize_claude_client(model_name='mistral', region="us-east-1"):
    """Initialize and return the Claude API client."""
    try:
        # Check for environment variables
        bedrock_access_key = os.environ.get('BEDROCK_ACCESS_KEY')
        bedrock_secret_access_key = os.environ.get('BEDROCK_SECRET_ACCESS_KEY')
        # print(bedrock_access_key, bedrock_secret_access_key)
        
        if not bedrock_access_key or not bedrock_secret_access_key:
            print("Warning: BEDROCK_ACCESS_KEY or BEDROCK_SECRET_ACCESS_KEY environment variables not set.")
            print("Using default AWS credential providers.")
        
        # Check if the module is available
        if AnthropicBedrock is None:
            print("Error: anthropics_bedrock module not available.")
            return None
        
        # Initialize the client
        claude_client = AnthropicBedrock(
            aws_access_key=bedrock_access_key,
            aws_secret_key=bedrock_secret_access_key,
            aws_region=region,# "us-east-1",# "us-west-2",
            max_retries=30  # Reduced for testing
        )
        
        return claude_client
    except Exception as e:
        print(f"Error initializing Claude client: {e}")
        return None

def call_claude_api(claude_client, prompt, model_name='claude', 
                     model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
                     max_retries=50, base_delay=0.5, thinking=False):
    """Call the Claude API with the given prompt, with retry logic for rate limiting.
    
    Args:
        claude_client: Initialized Claude client
        prompt: The prompt to send to Claude
        model: Claude model to use
        max_retries: Maximum number of retry attempts for rate limiting (default: 5)
        base_delay: Base delay in seconds for exponential backoff (default: 1.0)
        
    Returns:
        Claude's response text or error message
    """
    if not claude_client:
        print("Error: Claude client not initialized.")
        return "ERROR: API client not available"
    
    for attempt in range(max_retries + 1):
        try:
            # Make the API call
            if model_name == 'mistral':
                body = json.dumps({
                    "prompt": prompt,
                    "max_tokens": 4096,
                    "temperature": 0,
                    "top_p": 1,
                    "top_k": 200,
                    "stop_sequences": ["<USER_QUERY>",'<API_RESPONSE>','H:']
                })
                response = claude_client.invoke_model(body=body, modelId=model)
                response_body = json.loads(response.get('body').read())
                return response_body.get('outputs')[0]['text']
            
            
            elif thinking:
                message = claude_client.messages.create(
                    model=model,
                    temperature=1,
                    max_tokens=10000,
                    thinking={
                        "type": "enabled",
                        "budget_tokens": 2000
                    },
                    stop_sequences = ['<API_RESPONSE>','<USER_QUERY>','H:'],
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                for block in message.content:
                    if block.type == "text":
                        return block.text
                # Extract the response text
                prediction = message.content[0].text
                return prediction
            else:
                message = claude_client.messages.create(
                    model=model,
                    temperature=0,
                    max_tokens=10000,
                    stop_sequences = ['<API_RESPONSE>','<USER_QUERY>','H:'],
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                
                # Extract the response text
                prediction = message.content[0].text
                return prediction
            
        except Exception as e:
            error_str = str(e)
            
            # Check if this is a rate limiting error (429)
            is_rate_limit_error = (
                "503" in error_str or 
                "Bedrock is unable to process your request" in error_str or 
                "429" in error_str or 
                "Too many tokens" in error_str or
                "rate limit" in error_str.lower() or
                "throttle" in error_str.lower()
            )
            
            # If it's a rate limit error and we have retries left, wait and retry
            if is_rate_limit_error and attempt < max_retries:
                # Calculate delay with exponential backoff and jitter
                delay = base_delay * (2 ** attempt)
                jitter = random.uniform(0.1, 0.3) * delay  # Add 10-30% jitter
                total_delay = delay + jitter
                
                print(f"⚠️  Rate limit hit. Retrying in {total_delay:.1f}s... (attempt {attempt + 1}/{max_retries})")
                time.sleep(total_delay)
                continue
            
            # Either not a rate limit error, or we've exhausted retries
            if is_rate_limit_error:
                print(f"❌ Rate limit error persisted after {max_retries} retries: {error_str}")
            else:
                print(f"Error calling Claude API: {e}")
            
            return f"ERROR: {error_str}"




def extract_json_from_response(text: str) -> str:
    """Extract JSON array from Claude's response text."""
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


def validate_claude_response(response_text: str) -> List[Dict]:
    """
    Extract and validate JSON from Claude's response.
    
    Returns:
        List of valid trail dictionaries or empty list if parsing fails
    """
    if response_text.startswith("ERROR:"):
        print(f"Claude API error: {response_text}")
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
        print(f"Error parsing Claude response as JSON: {e}")
        print("Response was:", response_text[:200], "..." if len(response_text) > 200 else "")
        return []
    except Exception as e:
        print(f"Unexpected error validating Claude response: {e}")
        return []

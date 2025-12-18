"""
Claude API client for LLM Judge system.
Adapted from generate_complexity_scenarios_using_inst.ipynb
"""

import os
import configparser

# Check for Anthropic library availability
try:
    from anthropic import AnthropicBedrock
    print("AnthropicBedrock library found.")
    anthropic_bedrock_available = True
except ImportError:
    print("AnthropicBedrock library not found. Will try regular Anthropic client.")
    anthropic_bedrock_available = False
    try:
        from anthropic import Anthropic
        print("Anthropic library found.")
        anthropic_available = True
    except ImportError:
        print("WARNING: Neither AnthropicBedrock nor Anthropic client is available.")
        print("         You'll need to install one of them using pip:")
        print("         pip install anthropic")
        anthropic_available = False


def load_aws_credentials():
    """Load AWS credentials from environment variables or AWS credentials file."""
    access_key = None
    secret_key = None
    
    # Try loading from environment variables directly
    access_key = os.environ.get("BEDROCK_ACCESS_KEY") or os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("BEDROCK_SECRET_ACCESS_KEY") or os.environ.get("AWS_SECRET_ACCESS_KEY")
    
    # Try loading from .env file if python-dotenv is available
    if not access_key or not secret_key:
        try:
            from dotenv import load_dotenv
            # Look for .env file in the current directory
            load_dotenv()  
            access_key = os.environ.get("BEDROCK_ACCESS_KEY") or os.environ.get("AWS_ACCESS_KEY_ID")
            secret_key = os.environ.get("BEDROCK_SECRET_ACCESS_KEY") or os.environ.get("AWS_SECRET_ACCESS_KEY")
            print("Loaded credentials from .env file")
        except ImportError:
            print("python-dotenv not installed. Skipping .env file loading.")
    
    # If still not found, try AWS credentials file
    if not access_key or not secret_key:
        try:
            config = configparser.ConfigParser()
            config.read(os.path.expanduser("~/.aws/credentials"))
            if "default" in config:
                access_key = access_key or config["default"].get("aws_access_key_id")
                secret_key = secret_key or config["default"].get("aws_secret_access_key")
                print("Loaded credentials from AWS credentials file")
        except Exception as e:
            print(f"Could not read AWS credentials file: {str(e)}")
    
    if access_key and secret_key:
        print("AWS credentials found")
    else:
        print("AWS credentials not found")
        
    return access_key, secret_key


def create_bedrock_client(region="us-east-1", max_retries=10000):
    """Create a Bedrock client with credentials if available, otherwise use AWS credential provider chain."""
    if not anthropic_bedrock_available and not anthropic_available:
        print("ERROR: No Anthropic client available. Please install the required package.")
        return None
        
    try:
        if anthropic_bedrock_available:
            BEDROCK_ACCESS_KEY, BEDROCK_SECRET_ACCESS_KEY = load_aws_credentials()
        
            if BEDROCK_ACCESS_KEY and BEDROCK_SECRET_ACCESS_KEY:
                return AnthropicBedrock(
                    aws_access_key=BEDROCK_ACCESS_KEY,
                    aws_secret_key=BEDROCK_SECRET_ACCESS_KEY,
                    aws_region=region,
                    max_retries=max_retries
                )
            else:
                # Use default AWS credential provider chain
                return AnthropicBedrock(
                    aws_region=region,
                    max_retries=max_retries
                )
        else:  # Use regular Anthropic client
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                try:
                    from dotenv import load_dotenv
                    load_dotenv()
                    api_key = os.environ.get("ANTHROPIC_API_KEY")
                except ImportError:
                    pass
                    
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not found in environment variables!")
                    
            return Anthropic(api_key=api_key)
    except Exception as e:
        print(f"Error creating client: {str(e)}")
        return None


def claude_pred(client, prompt, model="claude-3-opus-20240229"):
    """Get a prediction from Claude API for LLM Judge evaluation."""
    try:
        # For AnthropicBedrock
        if hasattr(client, 'messages'):  # Bedrock client
            message = client.messages.create(
                model="us.anthropic.claude-opus-4-20250514-v1:0",  # Use Claude Opus for evaluation
                temperature=0.1,  # Low temperature for consistent evaluation
                max_tokens=2000,  # Sufficient for detailed evaluation
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            prediction = message.content[0].text
        else:  # Anthropic client
            message = client.messages.create(
                model=model,
                temperature=0.1,  # Low temperature for consistent evaluation
                max_tokens=2000,  # Sufficient for detailed evaluation
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            prediction = message.content[0].text
            
        return prediction
    except Exception as e:
        print(f"Error calling Claude API: {str(e)}")
        raise


def create_claude_client():
    """Create and return a Claude client for use in the LLM Judge system."""
    client = create_bedrock_client()
    
    if client is None:
        print("Failed to create client. Please check your credentials.")
        return None
    else:
        print(f"Client created successfully: {type(client).__name__}")
        return client

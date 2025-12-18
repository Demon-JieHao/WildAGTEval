#!/usr/bin/env python3
"""
Step-by-Step LLM API Evaluation Tool

This module evaluates LLM performance using step-by-step inference where the LLM
makes API calls one at a time and receives feedback before making the next decision.

Usage:
    python step_by_step_llm_evaluator.py path/to/conversation.jsonl
    python step_by_step_llm_evaluator.py path/to/conversation.jsonl --output results.json
"""

import json
import os
import sys
import re
import argparse
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
import time
import yaml
from freezegun import freeze_time

SAFE_IGNORE_LIST = ['botocore', 'boto3', 'urllib3', 'anthropic', 'anthropic_bedrock', 'requests', 'httpx']

# Import UncertaintyManager
try:
    from uncertainty_manager import UncertaintyManager
except ImportError:
    print("Warning: UncertaintyManager not found. Uncertainty features will be disabled.")
    UncertaintyManager = None

# region = "us-west-2"
# region = "us-east-1"
region = "eu-west-2"

# Modified to support optional LiteLLM mode
def setup_imports(use_litellm=False):
    """Setup imports dynamically based on whether LiteLLM is used"""
    if use_litellm:
        from utils.litellm_api import initialize_litellm_client, call_litellm_api
        from utils.user_context import load_data, create_user_context
        return initialize_litellm_client, call_litellm_api, load_data, create_user_context
    else:
        from utils.claude_api import initialize_claude_client, call_claude_api
        from utils.user_context import load_data, create_user_context
        return initialize_claude_client, call_claude_api, load_data, create_user_context

# Import the common invoke_tool function
from common import invoke_tool, register_environment
from common.shared_memory_service import SharedMemoryService

# Default model for Claude
model_name = 'claude'
DEFAULT_CLAUDE_MODEL = "None"

@dataclass
class StepResult:
    """Record of a single step in step-by-step inference"""
    step_number: int
    llm_response: str
    parsed_action: Dict[str, Any]
    api_call: Optional[Dict[str, Any]] = None
    api_result: Optional[str] = None
    api_success: Optional[bool] = None
    execution_time: float = 0.0
    timestamp: str = ""
    
    # Fields used only for Teacher Forcing evaluation
    ground_truth_api: Optional[Dict[str, Any]] = None
    ground_truth_result: Optional[str] = None
    ground_truth_success: Optional[bool] = None
    prediction_correct: Optional[bool] = None
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

class ConversationHistory:
    """Manages conversation history for step-by-step inference"""
    
    def __init__(self, system_prompt: str, user_query: str):
        self.system_prompt = system_prompt
        self.user_query = user_query
        self.steps = []
    
    def add_user_query(self):
        """Add the initial user query"""
        self.steps.append({
            "role": "user",
            "content": self.user_query
        })
    
    def add_new_query(self, query: str):
        """Add a new user query to existing conversation"""
        self.steps.append({
            "role": "user",
            "content": query
        })
    
    def add_llm_response(self, response: str):
        """Add LLM response"""
        self.steps.append({
            "role": "assistant", 
            "content": response
        })
    
    def add_api_result(self, api_call: Dict[str, Any], result: str, success: bool):
        """Add API execution result as API_RESPONSE message"""
        api_name = api_call.get('api', 'unknown')
        params = api_call.get('params', {})
        
        # Use the same format as InteractiveLLMEvaluator - API_RESPONSE tags
        # This should be system-level, not user input
        api_response_message = f"""<API_RESPONSE>
API Result: {result}
</API_RESPONSE>"""
        
        self.steps.append({
            "role": "system",
            "content": api_response_message
        })
    
    def get_full_prompt(self) -> str:
        """Get the complete conversation prompt"""
        prompt_parts = [self.system_prompt]
        
        for step in self.steps:
            if step["role"] == "user":
                prompt_parts.append(f"Human: {step['content']}")
            elif step["role"] == "assistant":
                prompt_parts.append(f"Assistant: {step['content']}")
            elif step["role"] == "system":
                # System messages (like API_RESPONSE) are added directly without prefix
                prompt_parts.append(step['content'])
        
        return "\n\n".join(prompt_parts)
    
    def get_context_stats(self) -> Dict[str, Any]:
        """Get statistics about the conversation context"""
        full_prompt = self.get_full_prompt()
        return {
            'total_chars': len(full_prompt),
            'estimated_tokens': len(full_prompt) // 4,  # Rough estimate: 4 chars per token
            'total_steps': len(self.steps),
            'user_queries': len([s for s in self.steps if s["role"] == "user"]),
            'assistant_responses': len([s for s in self.steps if s["role"] == "assistant"]),
            'api_responses': len([s for s in self.steps if s["role"] == "system"])
        }

class StepByStepLLMEvaluator:
    """
    Step-by-step LLM evaluator that executes API calls one at a time
    """
    
    def __init__(self, max_steps: int = 20, step_timeout: float = 30.0, 
                 uncertainty_config_path: str = None, model_id: str = None,
                 enable_thinking: bool = False, prompt_path: str = None,
                 use_litellm: bool = False):
        """Initialize the evaluator"""
        self.use_litellm = use_litellm
        # Initialize Claude or LiteLLM client
        initialize_fn, call_fn, load_data, create_user_context = setup_imports(use_litellm=self.use_litellm)
        self.call_llm_api = call_fn

        if self.use_litellm:
            self.llm_client = initialize_fn()
            print("✅ Using LiteLLM unified API client (Anthropic/OpenAI/Mistral compatible)")
        else:
            self.llm_client = initialize_fn(model_name='claude', region=region)
            if not self.llm_client:
                raise RuntimeError("Failed to initialize Claude client")
            print("✅ Using Claude Bedrock client (AWS Anthropic)")
        
        # Store enhanced options
        self.model_id = model_id
        self.enable_thinking = enable_thinking
        self.prompt_path = prompt_path
        
        self.centralized_prompt = self.load_centralized_prompt()
        self.api_environments = self.setup_all_api_environments()
        self.max_steps = max_steps
        self.step_timeout = step_timeout
        
        # Initialize UncertaintyManager
        self.uncertainty_manager = None
        if uncertainty_config_path and UncertaintyManager:
            try:
                self.uncertainty_manager = UncertaintyManager(uncertainty_config_path)
                print(f"✅ Loaded uncertainty config: {uncertainty_config_path}")
                self.uncertainty_manager.print_config_info()
            except Exception as e:
                print(f"⚠️ Failed to load uncertainty config: {e}")
                self.uncertainty_manager = None
        elif uncertainty_config_path and not UncertaintyManager:
            print("❌ UncertaintyManager not available. Install required dependencies.")
        
        # Display enhanced options info
        if self.model_id:
            print(f"🤖 Using custom model: {self.model_id}")
        if self.enable_thinking:
            print(f"🧠 Thinking mode: Enabled")
        if self.prompt_path:
            print(f"📝 Custom prompt: {self.prompt_path}")
        
    def load_centralized_prompt(self) -> str:
        """Load the centralized API prompt with step-by-step instructions"""
        try:
            # Use custom prompt path if provided, otherwise use default
            if self.prompt_path:
                prompt_path = Path(self.prompt_path)
                print(f"📝 Loading custom prompt from: {self.prompt_path}")
            else:
                prompt_path = Path("extracted_api/centralized_prompt.md")
            
            if prompt_path.exists():
                with open(prompt_path, 'r') as f:
                    base_prompt = f.read()
                    
                # Add step-by-step specific instructions using End of Turn pattern
                step_by_step_instruction = """

## CRITICAL: Sequential API Execution

**SEQUENTIAL PROCESSING - How You Work:**
1. Make ONE API call per response
2. Wait for API result before making next decision
3. Use API results to inform subsequent actions
4. Signal completion with "<End of Turn>" when user's request is fully satisfied

**STRICTLY FORBIDDEN - Never Do This:**
- NEVER add "User:" text to your responses
- NEVER simulate or invent user input 
- NEVER include fake conversation turns
- NEVER add text that appears to be from the user
- NEVER generate API_RESPONSE tags - these are system-only
- NEVER simulate API results or responses
- NEVER add fake <API_RESPONSE> data
- NEVER make multiple API calls in one response

**Your Response Must ONLY Contain:**
1. Your explanatory text (optional)
2. ONE API call wrapped in <API_CALL> </API_CALL> tags, OR
3. "<End of Turn>" to signal completion
4. Nothing else

**CRITICAL: API Call Wrapping**
You MUST wrap your API calls with opening tag <API_CALL> and closing tag </API_CALL> (with angle brackets)

**Correct API Call Format (ONE CALL ONLY):**
```json
<API_CALL>
{
  "api": "api_name_here",
  "params": {
    "parameter_name": "value"
  }
}
</API_CALL>
```

**Turn Completion Signal:**
```
<End of Turn>
```

**Sequential Execution Examples:**

*Example 1: Weather-based thermostat adjustment*
```
User: "Check weather and set thermostat accordingly"

Step 1:
Assistant: "I'll check the current weather first.
<API_CALL>
{
  "api": "weather_current",
  "params": {
    "location": "current"
  }
}
</API_CALL>"

After step 1, there will be an "<API_RESPONSE>...</API_RESPONSE>"

Step 2:
Assistant: "It's quite hot outside at 28°C. I'll set the thermostat to cool the house.
<API_CALL>
{
  "api": "temperature_set",
  "params": {
    "endpoints": ["5"],
    "temperature": 22
  }
}
</API_CALL>"

After step 2, there will be an "<API_RESPONSE>...</API_RESPONSE>"

Step 3:
Assistant: "Perfect! I've adjusted your thermostat to 22°C to keep you comfortable in this hot weather.
<End of Turn>"
```

*Example 2: Simple single API call*
```
User: Turn on the living room lights

Step 1:
Assistant: "I'll turn on the living room lights for you.
<API_CALL>
{
  "api": "power_on",
  "params": {
    "endpoints": ["1"]
  }
}
</API_CALL>

After step 1, there will be an "<API_RESPONSE>...</API_RESPONSE>"

Step 2:
Assistant: The living room lights are now on.
<End of Turn>
```

**Turn Completion Rules:**
- Use "<End of Turn>" when the user's request is fully satisfied
- Continue with more API calls if more actions are needed
- Always end with "<End of Turn>" - never leave a turn hanging

**Response Termination:**
End your response immediately after your API call or "<End of Turn>". Do not add any additional text, user input, or conversation continuation.
"""
                return base_prompt + step_by_step_instruction
            else:
                raise FileNotFoundError("Centralized prompt not found")
            
        except Exception as e:
            print(f"Warning: Could not load centralized prompt: {e}")
            return self._get_fallback_prompt()
    
    def _get_fallback_prompt(self) -> str:
        """Fallback prompt if centralized prompt not available"""
        return """# Multi-Domain Smart Assistant API Reference

You are a smart assistant with access to multiple domain APIs. Please use step-by-step approach to handle user requests.

Execute only one API call at a time, wait for the result, then decide the next step.

API Call Format:
<API_CALL>
{
  "api": "api_name",
  "params": {"param": "value"}
}
</API_CALL>

When task is completed, reply: TASK_COMPLETED: [completion description]
"""
    
    def setup_all_api_environments(self) -> Dict[str, Any]:
        """Setup and register all available API execution environments"""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            
            if current_dir not in sys.path:
                sys.path.insert(0, current_dir)
            
            environments = {}
            
            # List of environments to load
            env_configs = [
                ('SmartHomeEnv', 'SmartHomeEnv'),
                ('InformationControlEnv', 'InformationControlEnv'), 
                ('MediaControlEnv', 'MediaControlEnv'),
                ('TransactionEnv', 'TransactionEnv'),
                ('CulinaryControlEnv', 'CulinaryControlEnv'),
                ('CommunicationController', 'CommunicationController'),
                ('TimeNotificationEnv', 'TimeNotificationEnv'),
            ]
            
            for module_name, class_name in env_configs:
                try:
                    module = __import__(module_name)
                    env_class = getattr(module, class_name)
                    env_instance = env_class()
                    register_environment(module_name, env_instance)
                    environments[module_name] = env_instance
                    print(f"  ✓ {module_name} loaded and registered")
                except Exception as e:
                    print(f"  ⚠️ {module_name} not available: {e}")
            
            print(f"Successfully loaded and registered {len(environments)} API environments")
            return environments
            
        except Exception as e:
            print(f"Error setting up API environments: {e}")
            return {}
    
    def extract_user_id_from_filename(self, filename: str) -> str:
        """Extract user ID from JSONL filename"""
        match = re.search(r'Conv_([^_]+)_', filename)
        return match.group(1) if match else "user1"
    
    def set_user_for_all_environments(self, user_id: str):
        """Set current user for all loaded environments"""
        for env_name, env in self.api_environments.items():
            try:
                if hasattr(env, 'set_current_user'):
                    env.set_current_user(user_id)
                    print(f"  ✓ Set user {user_id} for {env_name}")
            except Exception as e:
                print(f"  ❌ Error setting user for {env_name}: {e}")
    
    def parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response to extract action"""
        action = {
            "type": "unknown",
            "content": response,
            "api_call": None,
            "completion_message": None
        }
        
        # Check for End of Turn completion signal (primary method)
        if '<End of Turn>' in response or '<END OF TURN>' in response.upper():
            action["type"] = "completion"
            action["completion_message"] = "End of Turn detected"
            return action
        
        # Check for API call
        api_call_pattern = r'<API_CALL>\s*(.*?)\s*</API_CALL>'
        api_match = re.search(api_call_pattern, response, re.DOTALL | re.IGNORECASE)
        
        if api_match:
            try:
                api_call = json.loads(api_match.group(1).strip())
                if isinstance(api_call, dict) and 'api' in api_call and 'params' in api_call:
                    action["type"] = "api_call"
                    action["api_call"] = api_call
                    return action
            except json.JSONDecodeError:
                pass
        
        # Fallback: Check for old TASK_COMPLETED patterns (for backward compatibility)
        completion_patterns = [
            r'TASK_COMPLETED:\s*(.*)',
            r'Task completed:\s*(.*)',
            r'Task is completed:\s*(.*)',
            r'Task finished:\s*(.*)',
        ]
        
        for pattern in completion_patterns:
            match = re.search(pattern, response, re.IGNORECASE | re.DOTALL)
            if match:
                action["type"] = "completion"
                action["completion_message"] = match.group(1).strip()
                return action
        
        # # Check for clarification or thinking
        # if any(keyword in response.lower() for keyword in ['need', 'please', 'how', 'can', 'could', 'would']):
        #     action["type"] = "clarification"
        # else:
        #     action["type"] = "thinking"
        
        return action
    
    @freeze_time("2025-06-18 12:00:00", tz_offset=0, ignore=SAFE_IGNORE_LIST)
    def execute_api_call(self, api_call: Dict[str, Any]) -> Tuple[str, bool, Dict[str, Any]]:
        """Execute an API call with uncertainty management and return result, success status, and uncertainty info"""
        api_name = api_call.get('api', '')
        params = api_call.get('params', {})
        
        if not api_name:
            return "Error: No API name provided", False, {}
        
        try:
            start_time = time.time()
            
            # Apply uncertainties if UncertaintyManager is available
            if self.uncertainty_manager:
                with self.uncertainty_manager.apply_uncertainties_for_api(api_name) as uncertainty_info:
                    result = invoke_tool(api_name, **params)
            else:
                result = invoke_tool(api_name, **params)
                uncertainty_info = {
                    'api_name': api_name,
                    'applied_uncertainties': [],
                    'uncertainty_types': [],
                    'has_uncertainties': False
                }
            
            execution_time = time.time() - start_time
            
            # Add uncertainty info to result if uncertainties were applied
            if uncertainty_info['has_uncertainties']:
                try:
                    parsed_result = json.loads(result)
                    # parsed_result['_uncertainty_info'] = {
                    #     'applied_uncertainties': uncertainty_info['applied_uncertainties'],
                    #     'uncertainty_types': uncertainty_info['uncertainty_types']
                    # }
                    result = json.dumps(parsed_result)
                    print(f"    🎲 Applied uncertainties: {', '.join(uncertainty_info['uncertainty_types'])}")
                except json.JSONDecodeError:
                    # If result is not JSON, we can't add uncertainty info to it
                    pass
            
            # Parse result to determine success
            try:
                parsed_result = json.loads(result)
                success = parsed_result.get('success', True)
            except json.JSONDecodeError:
                success = not ('error' in result.lower() or 'failed' in result.lower())
            
            return result, success, uncertainty_info
            
        except Exception as e:
            return f"API execution error: {str(e)}", False, {}
    
    def execute_step_by_step_inference(self, user_query: str, conversation: ConversationHistory = None,
                                     model: str = DEFAULT_CLAUDE_MODEL) -> List[StepResult]:
        """Execute step-by-step inference for a single query"""
        # Initialize conversation history if not provided
        if conversation is None:
            conversation = ConversationHistory(self.centralized_prompt, user_query)
            conversation.add_user_query()
        else:
            # Add new query to existing conversation
            conversation.add_new_query(user_query)
        
        steps = []
        
        for step_num in range(1, self.max_steps + 1):
            print(f"    Step {step_num}: Reasoning...")
            
            start_time = time.time()
            
            try:
                # Get LLM response
                full_prompt = conversation.get_full_prompt()
                llm_response = self.call_llm_api(
                    self.llm_client if not self.use_litellm else None,
                    full_prompt,
                    model_name=model_name,
                    model=model,
                    thinking=self.enable_thinking
                )
                
                # Parse the response
                parsed_action = self.parse_llm_response(llm_response)
                conversation.add_llm_response(llm_response)
                
                # Create step result
                step_result = StepResult(
                    step_number=step_num,
                    llm_response=llm_response,
                    parsed_action=parsed_action,
                    execution_time=time.time() - start_time
                )
                
                # Handle different action types
                if parsed_action["type"] == "completion":
                    print(f"    ✅ Task completed: {parsed_action['completion_message']}")
                    steps.append(step_result)
                    break
                
                elif parsed_action["type"] == "api_call":
                    api_call = parsed_action["api_call"]
                    print(f"    🔄 Executing API: {api_call['api']}")
                    
                    # Execute API call with uncertainty management
                    api_result, api_success, uncertainty_info = self.execute_api_call(api_call)
                    
                    # Update step result
                    step_result.api_call = api_call
                    step_result.api_result = api_result
                    step_result.api_success = api_success
                    
                    # Add API result to conversation
                    conversation.add_api_result(api_call, api_result, api_success)
                    
                    print(f"    {'✅' if api_success else '❌'} API result: {api_result[:100]}...")
                
                elif parsed_action["type"] == "clarification":
                    print(f"    ❓ LLM asking for clarification")
                    # In evaluation mode, we treat this as a completion
                    step_result.parsed_action["completion_message"] = "Need more information"
                    steps.append(step_result)
                    break
                
                else:  # thinking
                    print(f"    💭 LLM thinking...")
                
                steps.append(step_result)
                
            except Exception as e:
                print(f"    ❌ Error in step {step_num}: {e}")
                error_step = StepResult(
                    step_number=step_num,
                    llm_response=f"ERROR: {str(e)}",
                    parsed_action={"type": "error", "error": str(e)},
                    execution_time=time.time() - start_time
                )
                steps.append(error_step)
                break
        
        if len(steps) >= self.max_steps:
            print(f"    ⚠️ Reached maximum steps ({self.max_steps})")
        
        return steps
    
    def calculate_step_by_step_metrics(self, steps: List[StepResult], 
                                     expected_apis: List[Dict]) -> Dict[str, Any]:
        """Calculate metrics for step-by-step inference"""
        # Extract actual API sequence from steps
        actual_apis = []
        for step in steps:
            if step.api_call:
                actual_apis.append(step.api_call)
        
        # Basic accuracy metrics (reuse from original evaluator)
        metrics = self.calculate_basic_accuracy_metrics(expected_apis, actual_apis)
        
        # Step-by-step specific metrics
        total_steps = len(steps)
        api_steps = len([s for s in steps if s.api_call])
        completion_steps = len([s for s in steps if s.parsed_action.get("type") == "completion"])
        error_steps = len([s for s in steps if s.parsed_action.get("type") == "error"])
        
        # Efficiency metrics
        expected_api_count = len(expected_apis)
        step_efficiency = expected_api_count / total_steps if total_steps > 0 else 0
        api_efficiency = expected_api_count / api_steps if api_steps > 0 else 0
        
        # Success metrics
        successful_apis = len([s for s in steps if s.api_success])
        api_success_rate = successful_apis / api_steps if api_steps > 0 else 0
        
        # Task completion detection
        task_completed = any(s.parsed_action.get("type") == "completion" for s in steps)
        
        # Add step-by-step specific metrics
        metrics.update({
            "total_steps": total_steps,
            "api_steps": api_steps,
            "completion_steps": completion_steps, 
            "error_steps": error_steps,
            "step_efficiency": step_efficiency,
            "api_efficiency": api_efficiency,
            "api_success_rate": api_success_rate,
            "task_completed": task_completed,
            "inference_path": [s.parsed_action.get("type") for s in steps]
        })
        
        return metrics
    
    def calculate_basic_accuracy_metrics(self, expected_apis: List[Dict], 
                                       actual_apis: List[Dict]) -> Dict[str, Any]:
        """Calculate basic accuracy metrics (same as original evaluator)"""
        metrics = {
            'exact_sequence_match': expected_apis == actual_apis,
            'api_count_match': len(expected_apis) == len(actual_apis),
            'api_coverage_rate': 0.0,
            'redundancy_rate': 0.0,
            'api_name_accuracy': 0.0,
            'parameter_accuracy': 0.0,
            'order_accuracy': 0.0
        }
        
        if not expected_apis:
            return metrics
        
        # Calculate API coverage rate
        expected_api_names = [call.get('api', '') for call in expected_apis]
        actual_api_names = [call.get('api', '') for call in actual_apis]
        
        covered_apis = sum(1 for api in expected_api_names if api in actual_api_names)
        metrics['api_coverage_rate'] = covered_apis / len(expected_api_names)
        
        # Calculate redundancy rate
        if actual_apis:
            redundant_apis = len(actual_apis) - len(expected_apis)
            metrics['redundancy_rate'] = max(0, redundant_apis) / len(actual_apis)
        
        # Calculate API name accuracy
        min_length = min(len(expected_apis), len(actual_apis))
        correct_names = sum(1 for i in range(min_length) 
                          if expected_apis[i].get('api') == actual_apis[i].get('api'))
        metrics['api_name_accuracy'] = correct_names / len(expected_apis) if expected_apis else 0.0
        
        # Calculate parameter accuracy
        param_matches = 0
        total_params = 0
        
        for i in range(min_length):
            exp_params = expected_apis[i].get('params', {})
            act_params = actual_apis[i].get('params', {})
            
            if exp_params:
                total_params += len(exp_params)
                for key, value in exp_params.items():
                    if key in act_params and act_params[key] == value:
                        param_matches += 1
        
        metrics['parameter_accuracy'] = param_matches / total_params if total_params > 0 else 1.0
        
        return metrics
    
    def create_state_snapshot(self, memory_service) -> Dict[str, Any]:
        """Create a full snapshot of the current shared state for safe restoration."""
        import copy
        
        data = memory_service.get_data()
        
        # ⭐ Store the entire data using a deep copy
        full_snapshot = copy.deepcopy(data)
        
        print(f"    📸 Full state snapshot created ({len(full_snapshot)} keys)")
        return full_snapshot

    def restore_state_snapshot(self, memory_service, snapshot: Dict[str, Any]):
        """Fully restore the shared state from a previously saved snapshot."""
        import copy
        
        data = memory_service.get_data()
        # ⭐ Replace the entire data with the snapshot
        data.clear()
        data.update(copy.deepcopy(snapshot))  # data.update(snapshot)
        
        # Notify all observers about the full change
        memory_service.notify_observers(list(snapshot.keys()))
        print(f"    🔄 Full state restored ({len(snapshot)} keys)")

    def create_state_fingerprint(self, memory_service) -> str:
        """Create a lightweight fingerprint for the current state (for quick comparisons)."""
        import hashlib
        import json
        
        data = memory_service.get_data()
        
        # Convert the dictionary to a sorted JSON string and hash it
        try:
            sorted_data = json.dumps(data, sort_keys=True, default=str)
            fingerprint = hashlib.md5(sorted_data.encode()).hexdigest()[:16]
            return fingerprint
        except Exception as e:
            # If hash creation fails, create a simple identifier based on data size and key count
            return f"keys{len(data)}_size{len(str(data))}"

    def verify_state_integrity(self, memory_service, expected_snapshot: Dict[str, Any], 
                              operation_name: str) -> bool:
        """Verify state integrity by comparing current data to an expected snapshot."""
        current_data = memory_service.get_data()
        
        # Basic check: number of keys
        if len(current_data) != len(expected_snapshot):
            print(f"    ⚠️ {operation_name}: Key count mismatch! Current: {len(current_data)}, Expected: {len(expected_snapshot)}")
            return False
        
        # Key set check
        current_keys = set(current_data.keys())
        expected_keys = set(expected_snapshot.keys())
        if current_keys != expected_keys:
            missing_keys = expected_keys - current_keys
            extra_keys = current_keys - expected_keys
            print(f"    ⚠️ {operation_name}: Key set mismatch!")
            if missing_keys:
                print(f"      Missing keys: {list(missing_keys)[:3]}...")
            if extra_keys:
                print(f"      Extra keys: {list(extra_keys)[:3]}...")
            return False
        
        # Value check (sampling)
        mismatched_keys = []
        for key in list(expected_keys)[:5]:  # Check only the first 5 keys for performance
            if str(current_data.get(key)) != str(expected_snapshot.get(key)):
                mismatched_keys.append(key)
        
        if mismatched_keys:
            print(f"    ⚠️ {operation_name}: Value mismatch in keys: {mismatched_keys[:2]}...")
            return False
        
        print(f"    ✅ {operation_name}: State integrity verified!")
        return True

    def execute_teacher_forcing_step_safe(self, predicted_api: Dict, ground_truth_api: Dict) -> Tuple[str, str, bool, bool]:
        """Execute a Teacher Forcing step without state corruption"""
        
        # 1. Save a full snapshot of the state
        memory_service = SharedMemoryService.get_instance()
        state_snapshot = self.create_state_snapshot(memory_service)
        initial_fingerprint = self.create_state_fingerprint(memory_service)
        print(f"    🔍 Initial state fingerprint: {initial_fingerprint}")
        
        try:
            # 2. Execute the predicted API (for logging/evaluation)
            if predicted_api and predicted_api.get('api'):
                print(f"    📊 Executing predicted API for evaluation: {predicted_api['api']}")
                pred_result, pred_success, pred_uncertainty = self.execute_api_call(predicted_api)
                
                # Check state change after prediction execution
                post_prediction_fingerprint = self.create_state_fingerprint(memory_service)
                if post_prediction_fingerprint != initial_fingerprint:
                    print(f"    🔍 State changed after prediction: {initial_fingerprint} -> {post_prediction_fingerprint}")
                else:
                    print(f"    🔍 No state change from prediction execution")
            else:
                pred_result = "Error: No valid API predicted"
                pred_success = False
            
            # 3. ⭐ Core: restore the entire state from the snapshot (completely remove prediction effects)
            self.restore_state_snapshot(memory_service, state_snapshot)
            
            # Verify restoration
            restored_fingerprint = self.create_state_fingerprint(memory_service)
            restoration_success = self.verify_state_integrity(memory_service, state_snapshot, "State Restoration")
            
            if restored_fingerprint == initial_fingerprint and restoration_success:
                print(f"    ✅ State restoration verified: {restored_fingerprint}")
            else:
                print(f"    ⚠️ State restoration issue: {initial_fingerprint} -> {restored_fingerprint}")
            
            # 4. Execute the ground truth API (for actual state change)
            print(f"    ✅ Executing ground truth API for final state: {ground_truth_api['api']}")
            gt_result, gt_success, gt_uncertainty = self.execute_api_call(ground_truth_api)
            
            # Check final state
            final_fingerprint = self.create_state_fingerprint(memory_service)
            print(f"    🔍 Final state fingerprint: {final_fingerprint}")
            print(f"    🔍 State change from GT API: {restored_fingerprint} -> {final_fingerprint}")
            
            return pred_result, gt_result, pred_success, gt_success
            
        except Exception as e:
            # Ensure we always restore state on error
            print(f"    ⚠️ Error occurred, restoring state: {e}")
            self.restore_state_snapshot(memory_service, state_snapshot)
            
            # Verify restoration even in error scenarios
            error_restored_fingerprint = self.create_state_fingerprint(memory_service)
            if error_restored_fingerprint == initial_fingerprint:
                print(f"    ✅ Emergency state restoration successful: {error_restored_fingerprint}")
            else:
                print(f"    ❌ Emergency state restoration failed: {initial_fingerprint} -> {error_restored_fingerprint}")
            
            raise e

    def compare_api_predictions(self, predicted: Dict, ground_truth: Dict) -> bool:
        """Compare API prediction with ground truth"""
        if not predicted or not ground_truth:
            return False
        
        # Compare API name and core parameters
        return (predicted.get('api') == ground_truth.get('api') and 
                predicted.get('params', {}) == ground_truth.get('params', {}))

    def is_target_function_under_uncertainty(self, target_point: Dict) -> bool:
        """Check whether uncertainty is applied to the target function"""
        if not self.uncertainty_manager:
            return False
        
        target_function = target_point['function_name']
        
        try:
            # Get the list of APIs to which uncertainty is applied from UncertaintyManager
            uncertain_apis = set()
            config = self.uncertainty_manager.config
            
            for uncertainty_type, settings in config.get('uncertainties', {}).items():
                if settings.get('enabled', False):
                    apis = settings.get('apis', [])
                    uncertain_apis.update(apis)
            
            return target_function in uncertain_apis
            
        except Exception as e:
            print(f"    ⚠️ Error checking uncertainty for {target_function}: {e}")
            return False

    def is_target_function_in_uncertainty_context(self, target_point: Dict, target_config_path: str) -> bool:
        """Check whether the target function belongs to an uncertainty context (based on target_functions_config)"""
        try:
            import os
            import yaml
            
            # Extract uncertainty type from the target functions config filename
            config_filename = os.path.basename(target_config_path)
            
            # Known uncertainty types (detected from filename patterns)
            uncertainty_contexts = {
                'informational_notice': ['informational_notice', 'info_notice'],
                'feature_limitation': ['feature_limitation', 'featlimit'],
                'partially_irrelevant': ['partially_irrelevant', 'irrelevant'],
                'system_failure': ['system_failure'],
                'adhoc': ['adhoc']
            }
            
            # Extract uncertainty type from filename
            detected_uncertainty_type = None
            for uncertainty_type, patterns in uncertainty_contexts.items():
                for pattern in patterns:
                    if pattern in config_filename.lower():
                        detected_uncertainty_type = uncertainty_type
                        break
                if detected_uncertainty_type:
                    break
            
            # adhoc is not treated as an uncertainty context
            if detected_uncertainty_type == 'adhoc':
                return False
            
            # If no uncertainty context is detected, return False
            if not detected_uncertainty_type:
                return False
            
            # Load the target functions config file
            if not os.path.exists(target_config_path):
                print(f"    ⚠️ Target functions config not found: {target_config_path}")
                return False
            
            with open(target_config_path, 'r') as f:
                target_config = yaml.safe_load(f)
            
            target_functions = target_config.get('target_functions', [])
            target_function = target_point['function_name']
            
            # Check whether the target function belongs to the detected uncertainty context
            is_in_context = target_function in target_functions
            
            if is_in_context:
                print(f"    🎯 Target function {target_function} found in {detected_uncertainty_type} context")
            
            return is_in_context
            
        except Exception as e:
            print(f"    ⚠️ Error checking uncertainty context for {target_point.get('function_name', 'unknown')}: {e}")
            return False

    def has_disruptive_uncertainty(self, target_function: str) -> bool:
        """Check whether the uncertainty type is disruptive for cross-turn evaluation"""
        if not self.uncertainty_manager:
            return False
        
        # Uncertainty types that can disrupt cross-turn evaluation
        disruptive_types = {
            'SYSTEM_FAILURE_ERROR',      # System failure - state cannot be reliably predicted
            'FEATURE_LIMITATION_ERROR'   # Feature limitation - API behavior is blocked
        }
        
        try:
            config = self.uncertainty_manager.config
            
            for uncertainty_type, settings in config.get('uncertainties', {}).items():
                if (settings.get('enabled', False) and 
                    uncertainty_type in disruptive_types and
                    target_function in settings.get('apis', [])):
                    print(f"    🚫 Found disruptive uncertainty: {uncertainty_type} for {target_function}")
                    return True
            
            return False
            
        except Exception as e:
            print(f"    ⚠️ Error checking disruptive uncertainty for {target_function}: {e}")
            return False

    def is_problematic_error_line(self, data: Dict[str, Any]) -> bool:
        """Detect specific problematic error lines that should cause skip in Teacher Forcing modes"""
        
        # Condition 1: both error and message keys are present
        has_error_structure = ('error' in data and 'message' in data)
        
        # Condition 2: keys for normal conversation turns are missing
        missing_conversation_keys = ('query' not in data and 'api_sequence' not in data)
        
        # Condition 3: specific error message patterns (cart-related errors)
        cart_error_patterns = [
            "No products in cart",
            "Cart is empty", 
            "cannot update quantities"
        ]
        
        has_cart_error = False
        if 'error' in data or 'message' in data:
            error_text = str(data.get('error', '')) + str(data.get('message', ''))
            has_cart_error = any(pattern in error_text for pattern in cart_error_patterns)
        
        # Only treat as problematic when all conditions are satisfied
        return has_error_structure and missing_conversation_keys and has_cart_error

    def validate_conversation_file(self, file_path: str, evaluation_type: str) -> bool:
        """Validate JSONL file for Teacher Forcing modes - return False to trigger early exit"""
        
        # Only validate in Teacher Forcing modes
        should_check_errors = evaluation_type in ['teacher_forcing', 'turn_level_teacher_forcing']
        
        if not should_check_errors:
            return True  # Always pass in normal modes
        
        try:
            with open(file_path, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        data = json.loads(line)
                        
                        # Validate error lines only in Teacher Forcing modes
                        if self.is_problematic_error_line(data):
                            print(f"❌ [Teacher Forcing Mode] Problematic error line detected at line {line_num}")
                            print(f"   File: {file_path}")
                            print(f"   Error: {data.get('error')}")
                            print(f"   Message: {data.get('message')}")
                            print("   This conversation file will be skipped in Teacher Forcing evaluation.")
                            return False
                            
                    except json.JSONDecodeError as e:
                        print(f"❌ JSON parse error at line {line_num}: {e}")
                        return False
            
            return True  # Validation passed
            
        except Exception as e:
            print(f"❌ Error reading file {file_path}: {e}")
            return False

    def calculate_teacher_forcing_metrics(self, steps: List[StepResult], expected_apis: List[Dict]) -> Dict[str, Any]:
        """Calculate metrics specific to Teacher Forcing"""
        
        total_steps = len(steps)
        correct_predictions = sum(1 for step in steps if getattr(step, 'prediction_correct', False))
        
        return {
            'total_prediction_steps': total_steps,
            'correct_predictions': correct_predictions,
            'per_step_accuracy_rate': correct_predictions / total_steps if total_steps > 0 else 0,
            'step_by_step_accuracy': [getattr(step, 'prediction_correct', False) for step in steps]
        }

    def execute_teacher_forcing_inference(self, user_query: str, expected_api_sequence: List[Dict],
                                        conversation: ConversationHistory = None, 
                                        model: str = DEFAULT_CLAUDE_MODEL) -> List[StepResult]:
        """Safe Teacher Forcing inference - actually uses the safe function"""
        
        if conversation is None:
            conversation = ConversationHistory(self.centralized_prompt, user_query)
            conversation.add_user_query()
        else:
            conversation.add_new_query(user_query)
        
        steps = []
        
        for step_num, ground_truth_api in enumerate(expected_api_sequence, 1):
            print(f"    TF Step {step_num}: Safe prediction and execution...")
            
            start_time = time.time()
            
            try:
                # 1. Ask the LLM to predict the next API
                full_prompt = conversation.get_full_prompt()
                llm_response = self.call_llm_api(
                    self.llm_client if not self.use_litellm else None,
                    full_prompt,
                    model_name=model_name,
                    model=model,
                    thinking=self.enable_thinking
                )
                
                # 2. Parse the LLM response
                parsed_action = self.parse_llm_response(llm_response)
                predicted_api = parsed_action.get("api_call", {})
                
                # 3. ⭐ Actually use the safe execution function
                pred_result, gt_result, pred_success, gt_success = self.execute_teacher_forcing_step_safe(
                    predicted_api, ground_truth_api
                )
                
                # 4. Compute prediction correctness
                prediction_correct = self.compare_api_predictions(predicted_api, ground_truth_api)
                
                # 5. Create StepResult (compatible with analyzer)
                step_result = StepResult(
                    step_number=step_num,
                    llm_response=llm_response,
                    parsed_action=parsed_action,
                    api_call=predicted_api,        # LLM prediction (for analyzer)
                    api_result=pred_result,        # Predicted result (for analyzer) 
                    api_success=pred_success,      # Prediction success flag (for analyzer)
                    execution_time=time.time() - start_time
                )
                
                # Teacher Forcing specific information
                step_result.ground_truth_api = ground_truth_api
                step_result.ground_truth_result = gt_result
                step_result.ground_truth_success = gt_success
                step_result.prediction_correct = prediction_correct
                
                # 6. ⭐ Add only the ground truth result to the conversation (Teacher Forcing)
                conversation.add_api_result(ground_truth_api, gt_result, gt_success)
                
                print(f"    {'✅' if prediction_correct else '❌'} Prediction: {predicted_api.get('api', 'None')}")
                print(f"    ✅ Final state: Only ground truth effects remain")
                
                # 🔍 Debugging: data verification
                print(f"    🔍 DEBUG - step_result.api_call (for analyzer): {step_result.api_call}")
                print(f"    🔍 DEBUG - step_result.api_result (for analyzer): {step_result.api_result[:100] if step_result.api_result else 'None'}...")
                print(f"    🔍 DEBUG - GT API with full params: {ground_truth_api}")
                print(f"    🔍 DEBUG - conversation context uses GT: {ground_truth_api['api']} -> {gt_result[:50] if gt_result else 'None'}...")
                
                # 🔍 DEBUG: Conversation history (without system prompt)
                conversation_without_system = []
                for i, step in enumerate(conversation.steps):
                    conversation_without_system.append(f"  [{i+1}] {step['role']}: {step['content'][:80]}...")
                
                print(f"    🔍 DEBUG - Conversation history (without system prompt, last 3 entries):")
                for entry in conversation_without_system[-3:]:
                    print(f"      {entry}")
                
                steps.append(step_result)
                
            except Exception as e:
                print(f"    ❌ Error in safe TF step {step_num}: {e}")
                error_step = StepResult(
                    step_number=step_num,
                    llm_response=f"ERROR: {str(e)}",
                    parsed_action={"type": "error", "error": str(e)},
                    execution_time=time.time() - start_time
                )
                steps.append(error_step)
                break
        
        return steps

    def evaluate_single_query_teacher_forcing(self, query: str, expected_api_sequence: List[Dict], 
                                            conversation: ConversationHistory = None, 
                                            model: str = DEFAULT_CLAUDE_MODEL) -> Dict[str, Any]:
        """Evaluate a single query using Teacher Forcing - same interface as evaluate_single_query"""
        
        try:
            print(f"  🎓 Teacher Forcing evaluation for: {query[:50]}...")
            
            # Run Teacher Forcing inference
            steps = self.execute_teacher_forcing_inference(query, expected_api_sequence, conversation, model)
            
            # ⭐ Reuse existing metrics calculation (with additional TF-specific info)
            metrics = self.calculate_step_by_step_metrics(steps, expected_api_sequence)
            
            # Add Teacher Forcing specific metrics
            tf_metrics = self.calculate_teacher_forcing_metrics(steps, expected_api_sequence)
            metrics.update(tf_metrics)
            
            # Success judgment (Teacher Forcing criteria)
            prediction_success = tf_metrics.get("per_step_accuracy_rate", 0) >= 0.8
            task_understanding = metrics.get("task_completed", False)
            success = prediction_success and task_understanding
            
            return {
                'query': query,
                'expected_api_sequence': expected_api_sequence,
                'steps': [asdict(step) for step in steps],  # Compatible with transaction_accuracy_analyzer
                'metrics': metrics,
                'success': success,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'query': query,
                'expected_api_sequence': expected_api_sequence,
                'error': str(e),
                'success': False,
                'timestamp': datetime.now().isoformat()
            }

    def evaluate_jsonl_file_teacher_forcing(self, jsonl_path: str, model: str = DEFAULT_CLAUDE_MODEL) -> Dict[str, Any]:
        """Evaluate a JSONL file with Teacher Forcing - same structure as evaluate_jsonl_file"""
        
        print(f"\nEvaluating JSONL file with Teacher Forcing inference: {jsonl_path}")
        
        # Setup identical to the standard evaluation
        filename = os.path.basename(jsonl_path)
        user_id = self.extract_user_id_from_filename(filename)
        print(f"Extracted user ID: {user_id}")
        self.set_user_for_all_environments(user_id)
        
        # Shared conversation history
        conversation = ConversationHistory(self.centralized_prompt, "")
        print("📚 Using cumulative conversation history across queries (Teacher Forcing mode)")
        
        # Process JSONL file (same pattern as standard evaluation)
        query_results = []
        total_queries = 0
        
        try:
            with open(jsonl_path, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        data = json.loads(line)
                        query = data.get('query', '')
                        api_sequence = data.get('api_sequence', [])
                        
                        if not query or not api_sequence:
                            continue
                        
                        print(f"\n  TF Query {line_num}: {query[:60]}...")
                        
                        # ⭐ Teacher Forcing evaluation
                        result = self.evaluate_single_query_teacher_forcing(query, api_sequence, conversation, model)
                        result['line_number'] = line_num
                        query_results.append(result)
                        total_queries += 1
                        
                        # Context monitoring (same as standard evaluation)
                        context_stats = conversation.get_context_stats()
                        if context_stats['estimated_tokens'] > 100000:
                            print(f"  ⚠️ Context growing large: ~{context_stats['estimated_tokens']:,} tokens")
                        # elif total_queries % 5 == 0:
                        #     print(f"  📊 Context: ~{context_stats['estimated_tokens']:,} tokens, {context_stats['user_queries']} queries")
                        
                    except json.JSONDecodeError as e:
                        print(f"  Error parsing line {line_num}: {e}")
                        continue
        
        except Exception as e:
            return {'error': f"Error reading file: {e}", 'success': False}
        
        # File-level aggregation (similar to standard but with additional TF metrics)
        successful_queries = sum(1 for r in query_results if r.get('success', False))
        
        # Teacher Forcing specific aggregation
        total_predictions = sum(r.get('metrics', {}).get('total_prediction_steps', 0) for r in query_results)
        correct_predictions = sum(r.get('metrics', {}).get('correct_predictions', 0) for r in query_results)
        avg_tf_accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
        
        # Standard aggregations (for compatibility)
        avg_api_coverage = sum(r.get('metrics', {}).get('api_coverage_rate', 0) for r in query_results) / total_queries if total_queries > 0 else 0
        avg_api_accuracy = sum(r.get('metrics', {}).get('api_name_accuracy', 0) for r in query_results) / total_queries if total_queries > 0 else 0
        avg_param_accuracy = sum(r.get('metrics', {}).get('parameter_accuracy', 0) for r in query_results) / total_queries if total_queries > 0 else 0
        
        # Step-by-step metrics (for main() function compatibility)
        total_steps = sum(r.get('metrics', {}).get('total_steps', 0) for r in query_results)
        total_api_steps = sum(r.get('metrics', {}).get('api_steps', 0) for r in query_results)
        avg_step_efficiency = sum(r.get('metrics', {}).get('step_efficiency', 0) for r in query_results) / total_queries if total_queries > 0 else 0
        
        return {
            'evaluation_type': 'teacher_forcing_inference',
            'file_path': jsonl_path,
            'filename': filename,
            'user_id': user_id,
            'model': model,
            'total_queries': total_queries,
            'successful_queries': successful_queries,
            'success_rate': successful_queries / total_queries if total_queries > 0 else 0,
            
            # Standard compatibility metrics
            'avg_api_coverage_rate': avg_api_coverage,
            'avg_api_name_accuracy': avg_api_accuracy,
            'avg_parameter_accuracy': avg_param_accuracy,
            'overall_score': (avg_api_coverage + avg_api_accuracy + avg_param_accuracy) / 3,
            
            # Step-by-step metrics (for main function compatibility)
            'step_by_step_metrics': {
                'total_steps': total_steps,
                'total_api_steps': total_api_steps,
                'avg_steps_per_query': total_steps / total_queries if total_queries > 0 else 0,
                'avg_api_steps_per_query': total_api_steps / total_queries if total_queries > 0 else 0,
                'avg_step_efficiency': avg_step_efficiency
            },
            
            # Teacher Forcing specific metrics
            'teacher_forcing_metrics': {
                'total_prediction_steps': total_predictions,
                'correct_predictions': correct_predictions,
                'avg_prediction_accuracy': avg_tf_accuracy
            },
            
            'query_results': query_results,  # Fully compatible with transaction_accuracy_analyzer
            'evaluated_at': datetime.now().isoformat()
        }
    
    def evaluate_single_query(self, query: str, expected_api_sequence: List[Dict], 
                             conversation: ConversationHistory = None, model: str = DEFAULT_CLAUDE_MODEL) -> Dict[str, Any]:
        """Evaluate a single query using step-by-step inference"""
        try:
            print(f"  🔄 Step-by-step inference for: {query[:50]}...")
            
            # Execute step-by-step inference
            steps = self.execute_step_by_step_inference(query, conversation, model)
            
            # Calculate metrics
            metrics = self.calculate_step_by_step_metrics(steps, expected_api_sequence)
            
            # Determine overall success
            task_completed = metrics.get("task_completed", False)
            exact_match = metrics.get("exact_sequence_match", False)
            high_coverage = metrics.get("api_coverage_rate", 0) >= 0.8
            
            success = task_completed and (exact_match or high_coverage)
            
            return {
                'query': query,
                'expected_api_sequence': expected_api_sequence,
                'steps': [asdict(step) for step in steps],
                'metrics': metrics,
                'success': success,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'query': query,
                'expected_api_sequence': expected_api_sequence,
                'error': str(e),
                'success': False,
                'timestamp': datetime.now().isoformat()
            }
    
    def evaluate_jsonl_file(self, jsonl_path: str, model: str = DEFAULT_CLAUDE_MODEL) -> Dict[str, Any]:
        """Evaluate a JSONL file using step-by-step inference with cumulative conversation history"""
        print(f"\nEvaluating JSONL file with step-by-step inference: {jsonl_path}")
        
        # Extract user ID and set environments
        filename = os.path.basename(jsonl_path)
        user_id = self.extract_user_id_from_filename(filename)
        print(f"Extracted user ID: {user_id}")
        self.set_user_for_all_environments(user_id)
        
        # Create shared conversation history for the entire JSONL file
        conversation = ConversationHistory(self.centralized_prompt, "")
        print("📚 Using cumulative conversation history across queries")
        
        # Process JSONL file
        query_results = []
        total_queries = 0
        
        try:
            with open(jsonl_path, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        data = json.loads(line)
                        query = data.get('query', '')
                        api_sequence = data.get('api_sequence', [])
                        
                        if not query or not api_sequence:
                            continue
                        
                        print(f"\n  Query {line_num}: {query[:60]}...")
                        
                        # Evaluate with step-by-step inference using shared conversation
                        result = self.evaluate_single_query(query, api_sequence, conversation, model)
                        result['line_number'] = line_num
                        query_results.append(result)
                        total_queries += 1
                        
                        # Check conversation context length after each query
                        context_stats = conversation.get_context_stats()
                        if context_stats['estimated_tokens'] > 100000:  # Warning at ~100K tokens
                            print(f"  ⚠️ Context growing large: ~{context_stats['estimated_tokens']:,} tokens, {context_stats['total_steps']} steps")
                        # elif total_queries % 5 == 0:  # Show stats every 5 queries
                        #     print(f"  📊 Context: ~{context_stats['estimated_tokens']:,} tokens, {context_stats['user_queries']} queries processed")
                        
                    except json.JSONDecodeError as e:
                        print(f"  Error parsing line {line_num}: {e}")
                        continue
        
        except FileNotFoundError:
            return {'error': f"File not found: {jsonl_path}", 'success': False}
        except Exception as e:
            return {'error': f"Error reading file: {e}", 'success': False}
        
        # Calculate file-level summary
        successful_queries = sum(1 for r in query_results if r.get('success', False))
        
        # Aggregate step-by-step metrics
        total_steps = sum(r.get('metrics', {}).get('total_steps', 0) for r in query_results)
        total_api_steps = sum(r.get('metrics', {}).get('api_steps', 0) for r in query_results)
        avg_step_efficiency = sum(r.get('metrics', {}).get('step_efficiency', 0) for r in query_results) / total_queries if total_queries > 0 else 0
        
        # Traditional metrics
        avg_api_coverage = sum(r.get('metrics', {}).get('api_coverage_rate', 0) for r in query_results) / total_queries if total_queries > 0 else 0
        avg_api_accuracy = sum(r.get('metrics', {}).get('api_name_accuracy', 0) for r in query_results) / total_queries if total_queries > 0 else 0
        avg_param_accuracy = sum(r.get('metrics', {}).get('parameter_accuracy', 0) for r in query_results) / total_queries if total_queries > 0 else 0
        
        # Get uncertainty configuration summary
        uncertainty_config = {}
        if self.uncertainty_manager:
            uncertainty_config = self.uncertainty_manager.get_config_summary()
        
        return {
            'evaluation_type': 'step_by_step_inference',
            'file_path': jsonl_path,
            'filename': filename,
            'user_id': user_id,
            'model': model,
            'uncertainty_config': uncertainty_config,
            'total_queries': total_queries,
            'successful_queries': successful_queries,
            'success_rate': successful_queries / total_queries if total_queries > 0 else 0,
            'avg_api_coverage_rate': avg_api_coverage,
            'avg_api_name_accuracy': avg_api_accuracy,
            'avg_parameter_accuracy': avg_param_accuracy,
            'overall_score': (avg_api_coverage + avg_api_accuracy + avg_param_accuracy) / 3,
            'step_by_step_metrics': {
                'total_steps': total_steps,
                'total_api_steps': total_api_steps,
                'avg_steps_per_query': total_steps / total_queries if total_queries > 0 else 0,
                'avg_api_steps_per_query': total_api_steps / total_queries if total_queries > 0 else 0,
                'avg_step_efficiency': avg_step_efficiency
            },
            'query_results': query_results,
            'evaluated_at': datetime.now().isoformat()
        }

    def find_target_points(self, jsonl_path: str, target_functions: List[str], target_config_path: str = None) -> List[Dict]:
        """Find all locations where the target functions appear"""
        
        with open(jsonl_path, 'r') as f:
            conversation_data = [json.loads(line) for line in f if line.strip()]
        
        target_points = []
        all_found_functions = set()
        
        # ⭐ For duplicate checking - track functions that have already been added
        added_functions = set()
        
        # ⭐ Track counts per function
        function_counts = {}
        
        # ⭐ File-based limits
        function_limits = None
        is_unclear_config = target_config_path and 'target_functions_unclear.yaml' in target_config_path
        
        if is_unclear_config:
            function_limits = {
                'get_user_inventory': 1,  # Special limit
                'default': 4  # General limit
            }
            print(f"📋 Applying limits for unclear config: get_user_inventory=1, others=4")
        
        # Collect all API functions (for debugging)
        for turn_idx, turn_data in enumerate(conversation_data):
            api_sequence = turn_data.get('api_sequence', [])
            for api in api_sequence:
                all_found_functions.add(api['api'])
        
        # Find target points
        for turn_idx, turn_data in enumerate(conversation_data):
            api_sequence = turn_data.get('api_sequence', [])
            
            for step_idx, api in enumerate(api_sequence):
                if api['api'] in target_functions:
                    
                    # ⭐ New limit logic (file-based)
                    if function_limits:
                        current_count = function_counts.get(api['api'], 0)
                        limit = function_limits.get(api['api'], function_limits['default'])
                        
                        if current_count >= limit:
                            print(f"    📊 Skipping {api['api']} at Turn {turn_idx}, Step {step_idx} - reached limit ({current_count}/{limit})")
                            continue
                    
                    # ⭐ Existing duplicate check logic (uncertainty-based)
                    if self.should_skip_duplicate(api['api'], added_functions):
                        print(f"    🚫 Skipping duplicate {api['api']} at Turn {turn_idx}, Step {step_idx} - uncertainty-based")
                        continue
                    
                    # Determine evaluation scope
                    is_last_step = (step_idx == len(api_sequence) - 1)
                    has_next_turn = (turn_idx + 1 < len(conversation_data))
                    
                    target_points.append({
                        'turn_id': turn_idx,
                        'step_id': step_idx,
                        'function_name': api['api'],
                        'query': turn_data['query'],
                        'expected_apis': api_sequence,
                        'full_conversation': conversation_data,
                        'evaluation_scope': 'cross_turn' if (is_last_step and has_next_turn) else 'single_turn'
                    })
                    
                    # ⭐ Update counts
                    function_counts[api['api']] = function_counts.get(api['api'], 0) + 1
                    added_functions.add(api['api'])
        
        # ⭐ Edge case handling: no target functions found
        if not target_points:
            print(f"\n⚠️  WARNING: No target functions found in conversation!")
            print(f"📋 Available functions in conversation: {sorted(all_found_functions)}")
            print(f"🎯 Target functions in config: {target_functions}")
            print(f"💡 Suggestion: Update target_functions.yaml to include some of the available functions")
        else:
            print(f"✅ Found {len(target_points)} target points:")
            for i, tp in enumerate(target_points):
                print(f"   {i+1}. Turn {tp['turn_id']}, Step {tp['step_id']}: {tp['function_name']} ({tp['evaluation_scope']})")
        
        return target_points

    def should_skip_duplicate(self, function_name: str, added_functions: set) -> bool:
        """Duplicate skipping logic - prevent duplicates when system_failure or feature_limitation is applied"""
        if function_name != 'get_user_inventory':
            return False  # allow duplicate

        # Check whether the function has already been added
        if function_name in added_functions:
            
            # Check current uncertainty settings
            if self.uncertainty_manager:
                
                # Check whether system failure or feature limitation is enabled
                config = self.uncertainty_manager.config
                uncertainties = config.get('uncertainties', {})
                
                disruptive_types = ['SYSTEM_FAILURE_ERROR', 'FEATURE_LIMITATION_ERROR']
                
                for uncertainty_type, settings in uncertainties.items():
                    if (settings.get('enabled', False) and 
                        uncertainty_type in disruptive_types and
                        function_name in settings.get('apis', [])):
                        
                        print(f"    ⚠️ Found disruptive uncertainty {uncertainty_type} for {function_name}")
                        return True  # prevent duplicate addition
            
            # General duplicate case (no uncertainty)
            return True
        
        return False  # not a duplicate, allow addition

    def execute_turn_level_teacher_forcing(self, target_point: Dict, conversation: ConversationHistory, model: str, target_config_path: str = None) -> List[StepResult]:
        """Execute Turn-level Teacher Forcing"""
        
        steps = []
        target_turn_apis = target_point['expected_apis']
        full_conversation = target_point['full_conversation']
        
        # PHASE 1: Execute ground truth until the target point
        print(f"🎯 Phase 1: GT execution until Turn {target_point['turn_id']}, Step {target_point['step_id']}")
        
        # 1-1. Execute all previous turns using ground truth
        for prev_turn_idx in range(target_point['turn_id']):
            prev_turn_data = full_conversation[prev_turn_idx]
            conversation.add_new_query(prev_turn_data['query'])
            
            for api in prev_turn_data.get('api_sequence', []):
                result, success, _ = self.execute_api_call(api)
                conversation.add_api_result(api, result, success)
        
        # 1-2. Execute ground truth up to the target step of the target turn (range depends on uncertainty)
        conversation.add_new_query(target_point['query'])
        
        # Check whether uncertainty is applied to decide GT execution range (dual condition)
        has_uncertainty_config = self.is_target_function_under_uncertainty(target_point)
        has_uncertainty_context = False
        
        # Check uncertainty context from target functions config
        if target_config_path:
            has_uncertainty_context = self.is_target_function_in_uncertainty_context(target_point, target_config_path)
        
        # ! 2) force executing GTs just before target point (clean mode) if target_functions_config is adhoc
        is_adhoc_target = False
        if target_config_path:
            config_filename = os.path.basename(target_config_path).lower()
            if "adhoc" in config_filename:
                is_adhoc_target = True

        if is_adhoc_target:
            has_uncertainty_config = False
            has_uncertainty_context = False

        has_uncertainty = has_uncertainty_config or has_uncertainty_context
        
        if has_uncertainty:
            # Include the target step (execute GT with uncertainty)
            end_step = target_point['step_id'] + 1
            uncertainty_reasons = []
            if has_uncertainty_config:
                uncertainty_reasons.append("uncertainty config")
            if has_uncertainty_context:
                uncertainty_reasons.append("target context")
            print(f"    🎲 Uncertainty mode: GT execution includes target step (until step {target_point['step_id']}) - Reason: {', '.join(uncertainty_reasons)}")
        else:
            # Execute up to the step before the target (clean evaluation)
            end_step = target_point['step_id']
            print(f"    ✨ Clean mode: GT execution until target step (until step {target_point['step_id'] - 1})")
        
        for step_idx in range(end_step):
            api = target_turn_apis[step_idx]
            result, success, _ = self.execute_api_call(api)
            conversation.add_api_result(api, result, success)
            
            # Record GT execution steps as well
            step_result = StepResult(
                step_number=step_idx + 1,
                llm_response="[GT_EXECUTION]",
                parsed_action={"type": "gt_execution", "api_call": api},
                api_call=api,
                api_result=result,
                api_success=success
            )
            steps.append(step_result)
        
        # PHASE 2: Auto-regressive inference  
        inference_start_step = end_step  # Start LLM evaluation from where GT execution ends
        print(f"🤖 Phase 2: Complete auto-regressive inference from Step {inference_start_step} until LLM completion")
        
        # ⭐ Core change: do not limit by expected API count; run until LLM naturally finishes within max_steps
        base_step_number = len(steps)  # Start numbering after GT execution steps
        
        for inference_step in range(self.max_steps):  # Free to run within max_steps
            current_step_idx = inference_start_step + inference_step
            
            # Compare with expected API if available (compare when exists, continue otherwise)
            expected_api = None
            if current_step_idx < len(target_turn_apis):
                expected_api = target_turn_apis[current_step_idx]
            
            print(f"    Step {base_step_number + inference_step + 1}: LLM inference...")
            
            try:
                # LLM inference
                full_prompt = conversation.get_full_prompt()
                llm_response = self.call_llm_api(
                    self.llm_client if not self.use_litellm else None,
                    full_prompt,
                    model_name=model_name,
                    model=model,
                    thinking=self.enable_thinking
                )
                parsed_action = self.parse_llm_response(llm_response)
                
                step_result = StepResult(
                    step_number=base_step_number + inference_step + 1,
                    llm_response=llm_response,
                    parsed_action=parsed_action,
                    execution_time=0.0
                )
                
                # ⭐ Handle natural completion
                if parsed_action["type"] == "completion":
                    print(f"    ✅ LLM completed naturally: {parsed_action.get('completion_message', 'End of Turn')}")
                    step_result.api_call = None
                    step_result.api_result = None
                    step_result.api_success = None
                    step_result.ground_truth_api = expected_api
                    step_result.prediction_correct = None
                    steps.append(step_result)
                    break
                    
                elif parsed_action["type"] == "api_call":
                    predicted_api = parsed_action["api_call"]
                    print(f"    🔄 LLM predicted API: {predicted_api.get('api', 'unknown')}")
                    
                    # Execute API and update conversation
                    api_result, api_success, _ = self.execute_api_call(predicted_api)
                    conversation.add_llm_response(llm_response)
                    conversation.add_api_result(predicted_api, api_result, api_success)
                    
                    # Update step result
                    step_result.api_call = predicted_api
                    step_result.api_result = api_result
                    step_result.api_success = api_success
                    step_result.ground_truth_api = expected_api
                    step_result.prediction_correct = self.compare_api_predictions(predicted_api, expected_api) if expected_api else None
                    
                    print(f"    {'✅' if step_result.prediction_correct else '❌' if step_result.prediction_correct is not None else '➖'} GT comparison: {expected_api.get('api', 'None') if expected_api else 'None'}")
                    
                    steps.append(step_result)
                    
                elif parsed_action["type"] == "clarification":
                    print(f"    ❓ LLM asking for clarification - treating as completion")
                    step_result.api_call = None
                    step_result.api_result = None
                    step_result.api_success = None
                    step_result.ground_truth_api = expected_api
                    step_result.prediction_correct = None
                    steps.append(step_result)
                    break
                    
                else:  # thinking
                    print(f"    💭 LLM thinking - continuing...")
                    step_result.api_call = None
                    step_result.api_result = None
                    step_result.api_success = None
                    step_result.ground_truth_api = expected_api
                    step_result.prediction_correct = None
                    steps.append(step_result)
                    
            except Exception as e:
                print(f"    ❌ Error in inference step: {e}")
                error_step = StepResult(
                    step_number=base_step_number + inference_step + 1,
                    llm_response=f"ERROR: {str(e)}",
                    parsed_action={"type": "error", "error": str(e)},
                    execution_time=0.0,
                    ground_truth_api=expected_api
                )
                steps.append(error_step)
                break
        
        # Warn when max steps is reached
        if inference_step >= self.max_steps - 1:
            print(f"    ⚠️ Reached max steps ({self.max_steps}) in auto-regressive inference")
        
        # PHASE 3: Cross-turn evaluation (if needed) - returned as a separate result
        cross_turn_result = None
        if target_point['evaluation_scope'] == 'cross_turn':
            
            # ⭐ Uncertainty check: skip cross-turn evaluation if disruptive uncertainty is applied
            if (self.is_target_function_under_uncertainty(target_point) and 
                self.has_disruptive_uncertainty(target_point['function_name'])):
                
                print(f"🚫 SKIPPING Cross-turn evaluation: {target_point['function_name']} has disruptive uncertainty")
                print(f"   └── Target function failure makes next turn evaluation meaningless")
                cross_turn_result = None  # Skip cross-turn evaluation
                
            else:
                next_turn_idx = target_point['turn_id'] + 1
                if next_turn_idx < len(full_conversation):
                    print(f"🔄 Phase 3: Cross-turn evaluation for Turn {next_turn_idx}")
                    
                    next_turn_data = full_conversation[next_turn_idx]
                    conversation.add_new_query(next_turn_data['query'])
                    
                    # Execute the next turn step-by-step (auto-regressive)
                    next_turn_steps = self.execute_step_by_step_inference(next_turn_data['query'], conversation, model)
                    
                    # Compare with ground truth
                    for i, step in enumerate(next_turn_steps):
                        if i < len(next_turn_data['api_sequence']):
                            expected_api = next_turn_data['api_sequence'][i]
                            step.ground_truth_api = expected_api
                            step.prediction_correct = self.compare_api_predictions(step.api_call, expected_api) if step.api_call else False
                    
                    # ⭐ Create cross-turn result separately (same format as teacher_forcing_test.json)
                    cross_turn_result = {
                        'steps': [asdict(step) for step in next_turn_steps],
                        'query': next_turn_data['query'],
                        'expected_api_sequence': next_turn_data['api_sequence'],
                        'turn_id': next_turn_idx,
                        'related_to_target': f"Turn {target_point['turn_id']}, Step {target_point['step_id']}"
                    }
                else:
                    print(f"🔄 Phase 3: No next turn available for cross-turn evaluation")
        
        return steps, cross_turn_result

    def evaluate_jsonl_file_turn_level_tf(self, jsonl_path: str, target_config_path: str, model: str = DEFAULT_CLAUDE_MODEL) -> Dict[str, Any]:
        """Evaluate a JSONL file using Turn-Level Teacher Forcing"""
        
        print(f"\nEvaluating JSONL file with Turn-Level Teacher Forcing: {jsonl_path}")
        print(f"Target functions config: {target_config_path}")
        
        # Load YAML config
        import yaml
        with open(target_config_path, 'r') as f:
            target_config = yaml.safe_load(f)
        
        target_functions = target_config.get('target_functions', [])
        print(f"Target functions: {target_functions}")
        
        # Setup
        filename = os.path.basename(jsonl_path)
        user_id = self.extract_user_id_from_filename(filename)
        print(f"Extracted user ID: {user_id}")
        self.set_user_for_all_environments(user_id)
        
        # Find target points
        target_points = self.find_target_points(jsonl_path, target_functions, target_config_path)
        print(f"Found {len(target_points)} target points")
        
        evaluation_results = []
        
        # ⭐ Guarantee state snapshot independence
        memory_service = SharedMemoryService.get_instance()
        initial_snapshot = self.create_state_snapshot(memory_service)
        print(f"📸 Created initial state snapshot for independence")
        
        # Run evaluation for each target point
        for idx, target_point in enumerate(target_points):
            print(f"\n🎯 Evaluating Target Point {idx+1}/{len(target_points)}")
            print(f"   Function: {target_point['function_name']}")
            print(f"   Turn {target_point['turn_id']}, Step {target_point['step_id']}")
            print(f"   Scope: {target_point['evaluation_scope']}")
            
            try:
                # ⭐ Ensure full independence: restore initial state for each target point
                self.restore_state_snapshot(memory_service, initial_snapshot)
                print(f"   🔄 State restored to initial snapshot for independence")
                
                # Independent conversation history
                conversation = ConversationHistory(self.centralized_prompt, "")
                
                # Run Turn-Level TF (now also returns cross_turn_result)
                steps, cross_turn_result = self.execute_turn_level_teacher_forcing(target_point, conversation, model, target_config_path)
                
                # ⭐ Handle main result (only steps of the target turn)
                target_expected_apis = target_point['expected_apis'][target_point['step_id']:]  # APIs from target step onward
                
                metrics = self.calculate_step_by_step_metrics(steps, target_expected_apis)
                tf_metrics = self.calculate_teacher_forcing_metrics(steps, target_expected_apis)
                metrics.update(tf_metrics)
                
                # ⭐ Handle cross-turn information (included as an additional field, not a separate query_result)
                cross_turn_evaluation = None
                if cross_turn_result:
                    print(f"   🔄 Including cross-turn evaluation as additional field")
                    
                    # Compute cross-turn metrics
                    cross_turn_steps = [StepResult(**step_data) for step_data in cross_turn_result['steps']]
                    cross_metrics = self.calculate_step_by_step_metrics(cross_turn_steps, cross_turn_result['expected_api_sequence'])
                    cross_tf_metrics = self.calculate_teacher_forcing_metrics(cross_turn_steps, cross_turn_result['expected_api_sequence'])
                    cross_metrics.update(cross_tf_metrics)
                    
                    # Add cross-turn information as an additional field (not a separate query_result)
                    cross_turn_evaluation = {
                        'query': cross_turn_result['query'],
                        'expected_api_sequence': cross_turn_result['expected_api_sequence'],
                        'steps': cross_turn_result['steps'],  # already dicts
                        'metrics': cross_metrics,
                        'success': cross_metrics.get('per_step_accuracy_rate', 0) >= 0.7,
                        'turn_id': cross_turn_result['turn_id'],
                        'related_to_target': cross_turn_result['related_to_target']
                    }
                
                # ⭐ Save main query_result (same structure as teacher_forcing_test.json)
                result = {
                    'query': target_point['query'],
                    'expected_api_sequence': target_expected_apis,
                    'steps': [asdict(step) for step in steps],
                    'metrics': metrics,
                    'success': metrics.get('per_step_accuracy_rate', 0) >= 0.7,
                    'timestamp': datetime.now().isoformat(),
                    
                    # Turn-Level TF specific fields (additional information)
                    'target_function': target_point['function_name'],
                    'target_location': f"Turn {target_point['turn_id']}, Step {target_point['step_id']}",
                    'evaluation_scope': target_point['evaluation_scope'],
                    'evaluation_type': 'turn_level_teacher_forcing',
                    
                    # ⭐ Include cross-turn information (as an additional field, not a separate query_result)
                    'cross_turn_evaluation': cross_turn_evaluation
                }
                
                # ⭐ Save exactly once (number of target points = number of query_results)
                evaluation_results.append(result)
                
                print(f"   ✅ Completed - Accuracy: {metrics.get('per_step_accuracy_rate', 0):.2%}")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                # Always restore state even when errors occur
                self.restore_state_snapshot(memory_service, initial_snapshot)
                
                error_result = {
                    'target_function': target_point['function_name'],
                    'target_location': f"Turn {target_point['turn_id']}, Step {target_point['step_id']}",
                    'evaluation_scope': target_point['evaluation_scope'],
                    'query': target_point['query'],
                    'error': str(e),
                    'success': False,
                    'evaluation_type': 'turn_level_teacher_forcing',
                    'timestamp': datetime.now().isoformat()
                }
                evaluation_results.append(error_result)
        
        # Aggregate full results  
        successful_evaluations = sum(1 for r in evaluation_results if r.get('success', False))
        total_evaluations = len(evaluation_results)
        
        # Turn-Level TF specific metrics
        total_predictions = sum(r.get('metrics', {}).get('total_prediction_steps', 0) for r in evaluation_results if 'metrics' in r)
        correct_predictions = sum(r.get('metrics', {}).get('correct_predictions', 0) for r in evaluation_results if 'metrics' in r)
        avg_tf_accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
        
        # Aggregated metrics (same as teacher_forcing_test.json)
        avg_api_coverage = sum(r.get('metrics', {}).get('api_coverage_rate', 0) for r in evaluation_results if 'metrics' in r) / total_evaluations if total_evaluations > 0 else 0
        avg_api_accuracy = sum(r.get('metrics', {}).get('api_name_accuracy', 0) for r in evaluation_results if 'metrics' in r) / total_evaluations if total_evaluations > 0 else 0
        avg_param_accuracy = sum(r.get('metrics', {}).get('parameter_accuracy', 0) for r in evaluation_results if 'metrics' in r) / total_evaluations if total_evaluations > 0 else 0
        
        # Step-by-step metrics
        total_steps = sum(r.get('metrics', {}).get('total_steps', 0) for r in evaluation_results if 'metrics' in r)
        total_api_steps = sum(r.get('metrics', {}).get('api_steps', 0) for r in evaluation_results if 'metrics' in r)
        avg_step_efficiency = sum(r.get('metrics', {}).get('step_efficiency', 0) for r in evaluation_results if 'metrics' in r) / total_evaluations if total_evaluations > 0 else 0

        return {
            'evaluation_type': 'turn_level_teacher_forcing',
            'file_path': jsonl_path,
            'filename': filename,
            'user_id': user_id,
            'model': model,
            'total_queries': total_evaluations,  # ⭐ Same as teacher_forcing_test.json
            'successful_queries': successful_evaluations,  # ⭐ Same as teacher_forcing_test.json
            'success_rate': successful_evaluations / total_evaluations if total_evaluations > 0 else 0,
            
            # ⭐ Aggregated metrics identical to teacher_forcing_test.json
            'avg_api_coverage_rate': avg_api_coverage,
            'avg_api_name_accuracy': avg_api_accuracy,
            'avg_parameter_accuracy': avg_param_accuracy,
            'overall_score': (avg_api_coverage + avg_api_accuracy + avg_param_accuracy) / 3,
            
            # ⭐ Step-by-step metrics identical to teacher_forcing_test.json
            'step_by_step_metrics': {
                'total_steps': total_steps,
                'total_api_steps': total_api_steps,
                'avg_steps_per_query': total_steps / total_evaluations if total_evaluations > 0 else 0,
                'avg_api_steps_per_query': total_api_steps / total_evaluations if total_evaluations > 0 else 0,
                'avg_step_efficiency': avg_step_efficiency
            },
            
            # ⭐ Teacher Forcing metrics identical to teacher_forcing_test.json
            'teacher_forcing_metrics': {
                'total_prediction_steps': total_predictions,
                'correct_predictions': correct_predictions,
                'avg_prediction_accuracy': avg_tf_accuracy
            },
            
            'query_results': evaluation_results,  # ⭐ Stored as query_results for compatibility
            'evaluated_at': datetime.now().isoformat()
        }

    def save_turn_level_results(self, results: List[Dict], output_dir: str, base_filename: str, 
                               jsonl_path: str, filename: str, user_id: str, model: str):
        """Save Turn-Level TF results as N individual files (expanding cross-turn into an independent level)"""
        os.makedirs(output_dir, exist_ok=True)
        
        uncertainty_config = {}
        if self.uncertainty_manager:
            uncertainty_config = self.uncertainty_manager.get_config_summary()
        
        for result in results:
            function_name = result['target_function']
            location = result['target_location'].replace(' ', '').replace(',', '_')
            filename_output = f"{base_filename}_TurnLevelTF_{location}_{function_name}.json"
            filepath = os.path.join(output_dir, filename_output)
            
            # ⭐ If cross-turn evaluation exists, expand it to an independent query_results level
            query_results = [result]  # Main query_results[0]
            total_queries = 1
            successful_queries = 1 if result.get('success', False) else 0
            
            if result.get('cross_turn_evaluation'):
                print(f"   🔄 Expanding cross-turn to independent query_results level")
                
                # Add cross-turn as query_results[1] (teacher_forcing_test.json format)
                cross_turn_eval = result['cross_turn_evaluation']
                query_results.append(cross_turn_eval)
                total_queries = 2
                
                # Aggregate success (main + cross-turn)
                if cross_turn_eval.get('success', False):
                    successful_queries += 1
                
                # Remove cross_turn_evaluation field from main result (avoid duplication)
                main_result = {k: v for k, v in result.items() if k != 'cross_turn_evaluation'}
                query_results[0] = main_result
            
            # ⭐ Save with a structure identical to teacher_forcing_test.json
            single_result = {
                'evaluation_type': 'turn_level_teacher_forcing',
                'file_path': jsonl_path,
                'filename': filename,
                'user_id': user_id,
                'model': model,
                'uncertainty_config': uncertainty_config,
                'total_queries': total_queries,
                'successful_queries': successful_queries,
                'success_rate': successful_queries / total_queries if total_queries > 0 else 0.0,
                
                # Aggregated metrics across main + cross-turn
                'avg_api_coverage_rate': sum(q.get('metrics', {}).get('api_coverage_rate', 0) for q in query_results if 'metrics' in q) / total_queries if total_queries > 0 else 0,
                'avg_api_name_accuracy': sum(q.get('metrics', {}).get('api_name_accuracy', 0) for q in query_results if 'metrics' in q) / total_queries if total_queries > 0 else 0,
                'avg_parameter_accuracy': sum(q.get('metrics', {}).get('parameter_accuracy', 0) for q in query_results if 'metrics' in q) / total_queries if total_queries > 0 else 0,
                'overall_score': 0,  # set after calculation
                
                # Step-by-step metrics aggregation
                'step_by_step_metrics': {
                    'total_steps': sum(q.get('metrics', {}).get('total_steps', 0) for q in query_results if 'metrics' in q),
                    'total_api_steps': sum(q.get('metrics', {}).get('api_steps', 0) for q in query_results if 'metrics' in q),
                    'avg_steps_per_query': 0,  # set after calculation
                    'avg_api_steps_per_query': 0,  # set after calculation
                    'avg_step_efficiency': sum(q.get('metrics', {}).get('step_efficiency', 0) for q in query_results if 'metrics' in q) / total_queries if total_queries > 0 else 0
                },
                
                # Teacher Forcing metrics aggregation
                'teacher_forcing_metrics': {
                    'total_prediction_steps': sum(q.get('metrics', {}).get('total_prediction_steps', 0) for q in query_results if 'metrics' in q),
                    'correct_predictions': sum(q.get('metrics', {}).get('correct_predictions', 0) for q in query_results if 'metrics' in q),
                    'avg_prediction_accuracy': 0  # set after calculation
                },
                
                'query_results': query_results,  # ⭐ Key point: cross-turn is stored as an independent level
                'evaluated_at': datetime.now().isoformat()
            }
            
            # Set calculated metrics
            single_result['overall_score'] = (single_result['avg_api_coverage_rate'] + single_result['avg_api_name_accuracy'] + single_result['avg_parameter_accuracy']) / 3
            
            step_metrics = single_result['step_by_step_metrics']
            step_metrics['avg_steps_per_query'] = step_metrics['total_steps'] / total_queries if total_queries > 0 else 0
            step_metrics['avg_api_steps_per_query'] = step_metrics['total_api_steps'] / total_queries if total_queries > 0 else 0
            
            tf_metrics = single_result['teacher_forcing_metrics']
            tf_metrics['avg_prediction_accuracy'] = tf_metrics['correct_predictions'] / tf_metrics['total_prediction_steps'] if tf_metrics['total_prediction_steps'] > 0 else 0
            
            with open(filepath, 'w') as f:
                json.dump(single_result, f, indent=2)
            print(f"✅ Saved: {filename_output} (queries: {total_queries})")
    
    def is_file_complete(self, filepath: str) -> bool:
        """Check whether the file is a complete JSON file"""
        try:
            if not os.path.exists(filepath):
                return False
            
            # Check file size (too small may indicate incompleteness)
            if os.path.getsize(filepath) < 100:  # Less than 100 bytes is considered incomplete
                return False
            
            # Check if JSON can be parsed
            with open(filepath, 'r') as f:
                data = json.load(f)
                
            # Check for required fields
            required_fields = ['evaluation_type', 'total_queries', 'query_results']
            for field in required_fields:
                if field not in data:
                    return False
            
            return True
            
        except (json.JSONDecodeError, IOError) as e:
            return False
    
    def check_output_file_exists(self, output_path: str) -> bool:
        """Check whether output file exists for normal/Teacher Forcing modes"""
        if not output_path:
            return False
        
        return self.is_file_complete(output_path)
    
    def get_turn_level_output_files(self, jsonl_path: str, target_config_path: str, output_dir: str) -> List[str]:
        """Generate list of expected output files for Turn-Level TF"""
        try:
            # Load YAML config
            with open(target_config_path, 'r') as f:
                target_config = yaml.safe_load(f)
            target_functions = target_config.get('target_functions', [])
            
            # Find target points
            target_points = self.find_target_points(jsonl_path, target_functions)
            
            # Generate expected output file list
            base_filename = Path(jsonl_path).stem
            expected_files = []
            
            for target_point in target_points:
                function_name = target_point['function_name']
                location = f"Turn{target_point['turn_id']}_Step{target_point['step_id']}"
                filename = f"{base_filename}_TurnLevelTF_{location}_{function_name}.json"
                filepath = os.path.join(output_dir, filename)
                expected_files.append(filepath)
            
            return expected_files
            
        except Exception as e:
            print(f"⚠️ Error getting expected output files: {e}")
            return []
    
    def check_turn_level_output_exists(self, jsonl_path: str, target_config_path: str, output_dir: str) -> bool:
        """Check that all output files exist for Turn-Level TF mode"""
        if not output_dir:
            return False
        
        expected_files = self.get_turn_level_output_files(jsonl_path, target_config_path, output_dir)
        
        if not expected_files:
            return False
        
        # Check that all files exist and are complete
        for filepath in expected_files:
            if not self.is_file_complete(filepath):
                return False
        
        return True

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Step-by-Step LLM API Evaluation Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Evaluate with step-by-step inference
  python step_by_step_llm_evaluator_exec_complexity.py path/to/file.jsonl
  
  # Custom output and model
  python step_by_step_llm_evaluator_exec_complexity.py path/to/file.jsonl --output results.json --model claude-3-haiku
  
  # Adjust inference parameters
  python step_by_step_llm_evaluator_exec_complexity.py path/to/file.jsonl --max-steps 15 --timeout 60
  
  # Enable uncertainties with YAML configuration
  python step_by_step_llm_evaluator_exec_complexity.py path/to/file.jsonl --uncertainty-config uncertainty_configs/all_uncertainties.yaml
  
  # Feature limitation errors only
  python step_by_step_llm_evaluator_exec_complexity.py path/to/file.jsonl --uncertainty-config uncertainty_configs/feature_limitation_only.yaml
  
  # Partially irrelevant information only
  python step_by_step_llm_evaluator_exec_complexity.py path/to/file.jsonl --uncertainty-config uncertainty_configs/partially_irrelevant_only.yaml
        """
    )
    
    parser.add_argument('jsonl_file', help='JSONL file to evaluate')
    parser.add_argument('--model', default=DEFAULT_CLAUDE_MODEL, help='Claude model to use')
    parser.add_argument('--output', '-o', help='Output file for results (JSON)')
    parser.add_argument('--max-steps', type=int, default=20, help='Maximum steps per query')
    parser.add_argument('--timeout', type=float, default=30.0, help='Timeout per step (seconds)')
    parser.add_argument('--model-id', help='Model ID to use (overrides default)')
    parser.add_argument('--enable-thinking', action='store_true', help='Enable thinking mode for enhanced reasoning')
    parser.add_argument('--prompt-path', help='Path to custom centralized prompt file')
    parser.add_argument('--uncertainty-config', help='YAML file path for uncertainty configuration')
    parser.add_argument('--teacher-forcing', action='store_true', help='Use Teacher Forcing evaluation')
    parser.add_argument('--turn-level-tf', action='store_true', help='Use Turn-Level Teacher Forcing evaluation')
    parser.add_argument('--target-functions-config', help='YAML file path for target functions configuration')
    parser.add_argument('--use-litellm', action='store_true', help='Use LiteLLM API instead of Claude Bedrock')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed output')
    parser.add_argument('--force', '-f', action='store_true', help='Force re-evaluation even if output files already exist')
    
    args = parser.parse_args()
    print(args)
    
    print("="*80)
    print(" Step-by-Step LLM API Evaluation Tool ".center(80, "="))
    print("="*80)
    
    try:
        # Initialize evaluator
        print("\nInitializing step-by-step evaluator...")
        
        # Use model-id if provided, otherwise use default model
        model_to_use = args.model_id if args.model_id else args.model
        
        evaluator = StepByStepLLMEvaluator(
            max_steps=args.max_steps,
            step_timeout=args.timeout,
            uncertainty_config_path=args.uncertainty_config,
            model_id=args.model_id,
            enable_thinking=args.enable_thinking,
            prompt_path=args.prompt_path,
            use_litellm=args.use_litellm
        )
        
        # Run evaluation
        print(f"Model: {model_to_use}")
        print(f"Max steps per query: {args.max_steps}")
        print(f"Step timeout: {args.timeout}s")
        if args.use_litellm:
            print("🧠 LiteLLM mode enabled (OpenAI API)")
        
        # Add safe data loading with early exit for Teacher Forcing modes
        evaluation_type = None
        if args.turn_level_tf:
            evaluation_type = 'turn_level_teacher_forcing'
        elif args.teacher_forcing:
            evaluation_type = 'teacher_forcing'
        else:
            evaluation_type = 'autoregressive'
        
        # Pre-validate JSONL file for Teacher Forcing modes
        if evaluation_type in ['teacher_forcing', 'turn_level_teacher_forcing']:
            if not evaluator.validate_conversation_file(args.jsonl_file, evaluation_type):
                print("❌ JSONL file contains problematic data for Teacher Forcing evaluation.")
                print("   Exiting gracefully...")
                sys.exit(0)
        
        # 🚫 Skip logic: Check if output files already exist (unless --force is used)
        if not args.force and args.output:
            if evaluation_type == 'turn_level_teacher_forcing':
                # Turn-Level TF: Check if all expected output files exist
                if args.target_functions_config:
                    output_dir = str(Path(args.output).parent)
                    if evaluator.check_turn_level_output_exists(args.jsonl_file, args.target_functions_config, output_dir):
                        expected_files = evaluator.get_turn_level_output_files(args.jsonl_file, args.target_functions_config, output_dir)
                        print(f"✅ All output files already exist ({len(expected_files)} files):")
                        for filepath in expected_files[:3]:  # Show first 3 files
                            print(f"   📄 {os.path.basename(filepath)}")
                        if len(expected_files) > 3:
                            print(f"   ... and {len(expected_files) - 3} more files")
                        print("📋 Skipping evaluation. Use --force to re-evaluate.")
                        sys.exit(0)
            else:
                # Normal/Teacher Forcing: Check single output file
                if evaluator.check_output_file_exists(args.output):
                    print(f"✅ Output file already exists: {args.output}")
                    print("📋 Skipping evaluation. Use --force to re-evaluate.")
                    sys.exit(0)
        
        # Choose evaluation method based on flags (priority: turn-level-tf > teacher-forcing > auto-regressive)
        if args.turn_level_tf and args.target_functions_config:
            print("🎯 Using Turn-Level Teacher Forcing evaluation mode")
            print(f"Target config: {args.target_functions_config}")
            results = evaluator.evaluate_jsonl_file_turn_level_tf(args.jsonl_file, args.target_functions_config, model_to_use)
            
            # ⭐ Add logic to save N files
            if args.output:
                base_filename = Path(args.jsonl_file).stem
                output_dir = Path(args.output).parent
                evaluator.save_turn_level_results(
                    results['query_results'], 
                    str(output_dir), 
                    base_filename,
                    args.jsonl_file,
                    results['filename'],
                    results['user_id'],
                    model_to_use
                )
                print(f"\n💾 Turn-Level TF results saved to: {output_dir}")
        elif args.teacher_forcing:
            print("🎓 Using Teacher Forcing evaluation mode")
            results = evaluator.evaluate_jsonl_file_teacher_forcing(args.jsonl_file, model_to_use)
        else:
            print("🔄 Using Auto-regressive evaluation mode")
            results = evaluator.evaluate_jsonl_file(args.jsonl_file, model_to_use)
        
        if 'error' in results:
            print(f"Error: {results['error']}")
            sys.exit(1)
        
        # Display summary - Turn-Level TF vs other evaluation types
        print(f"\n" + "="*60)
        print(" STEP-BY-STEP EVALUATION SUMMARY ".center(60, "="))
        print("="*60)
        print(f"File: {results['filename']}")
        print(f"User ID: {results['user_id']}")
        
        # ⭐ All evaluation modes now share the same structure (identical to teacher_forcing_test.json)
        print(f"Total Queries: {results['total_queries']}")
        print(f"Successful Queries: {results['successful_queries']}")
        print(f"Success Rate: {results['success_rate']:.2%}")
        print(f"Overall Score: {results['overall_score']:.2%}")
        
        # Display uncertainty information if available
        uncertainty_config = results.get('uncertainty_config', {})
        if uncertainty_config:
            print(f"\nUncertainty Configuration:")
            print(f"  Config: {uncertainty_config.get('config_name', 'Unknown')}")
            print(f"  Description: {uncertainty_config.get('config_description', 'No description')}")
            enabled_types = uncertainty_config.get('enabled_uncertainty_types', [])
            if enabled_types:
                print(f"  Enabled Types: {', '.join(enabled_types)}")
            stats = uncertainty_config.get('statistics', {})
            if stats:
                print(f"  APIs with Uncertainties: {stats.get('total_apis_with_uncertainties', 0)}")
                print(f"  Total Environment Variables: {stats.get('total_active_env_vars', 0)}")
        else:
            print(f"\nUncertainty Configuration: None (Clean evaluation)")
        
        # Step-by-step specific metrics - Turn-Level TF vs other evaluation types
        if results.get('evaluation_type') == 'turn_level_teacher_forcing':
            tf_metrics = results.get('turn_level_tf_metrics', {})
            print(f"\nTurn-Level Teacher Forcing Metrics:")
            print(f"  Total Prediction Steps: {tf_metrics.get('total_prediction_steps', 0)}")
            print(f"  Correct Predictions: {tf_metrics.get('correct_predictions', 0)}")
            print(f"  Prediction Accuracy: {tf_metrics.get('avg_prediction_accuracy', 0):.2%}")
        else:
            # General step-by-step metrics
            step_metrics = results['step_by_step_metrics']
            print(f"\nStep-by-Step Metrics:")
            print(f"  Total Steps: {step_metrics['total_steps']}")
            print(f"  Total API Steps: {step_metrics['total_api_steps']}")
            print(f"  Avg Steps per Query: {step_metrics['avg_steps_per_query']:.1f}")
            print(f"  Avg API Steps per Query: {step_metrics['avg_api_steps_per_query']:.1f}")
            print(f"  Step Efficiency: {step_metrics['avg_step_efficiency']:.2%}")
        
        if args.verbose:
            print(f"\n" + "="*60)
            print(" DETAILED RESULTS ".center(60, "="))
            print("="*60)
            
            for result in results['query_results']:
                print(f"\nQuery {result.get('line_number', '?')}: {result['query'][:60]}...")
                if result.get('success'):
                    print(f"  ✓ Success")
                else:
                    print(f"  ✗ Failed")
                
                metrics = result.get('metrics', {})
                steps = result.get('steps', [])
                print(f"  Steps: {len(steps)}")
                print(f"  API Coverage: {metrics.get('api_coverage_rate', 0):.2%}")
                print(f"  Task Completed: {metrics.get('task_completed', False)}")
        
        # Save results if output file specified
        if (args.output) and (not args.turn_level_tf):
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\nResults saved to: {output_path}")
        
        print("="*80)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

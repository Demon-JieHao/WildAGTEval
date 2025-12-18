#!/usr/bin/env python3
"""
Unified Analyzer

A unified analyzer for evaluating conversation test results across different domains.
Based on Multi-tool's side-effect vs non-side-effect API classification approach.

Key Features:
1. Side-effect APIs (state-changing) - strict validation
2. Non-side-effect APIs (query) - lenient validation  
3. Special case handling via configuration
4. Ad-hoc mode for repeated failure detection
5. Domain-agnostic validation logic

Usage:
    python unified_analyzer.py <test_result_file.json> -o <output_folder>
    python unified_analyzer.py <test_result_folder> --batch -o <output_folder>
    python unified_analyzer.py <test_result_folder> --batch --ad_hoc -o <output_folder>
"""

import os
import sys
import json
import argparse
import yaml
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from collections import defaultdict, Counter
import re


@dataclass
class UnifiedAPICall:
    """Unified representation of an API call"""
    api: str
    params: Dict[str, Any]
    is_side_effect: bool = False
    domain: str = "unknown"
    
    def matches(self, other: 'UnifiedAPICall', strict_params: bool = True) -> bool:
        """Check if this API call matches another"""
        if self.api != other.api:
            return False
        
        if not strict_params:
            return True
            
        # For strict parameter matching, check key parameters
        return self._params_match(self.params, other.params)
    
    def _params_match(self, expected: Dict, actual: Dict) -> bool:
        """Check if parameters match with some flexibility"""
        # Get key parameters for this API
        key_params = self._get_key_params(self.api)
        
        if not key_params:
            # If no key params defined, only check if function was called (don't validate parameters)
            return True
        
        # Otherwise, only validate key parameters
        for param in key_params:
            if param in expected:
                if param not in actual:
                    return False
                
                # Special handling for location parameters in weather APIs (case-insensitive), 'new_york' and 'New_York"
                if param == 'location' and self.api in ['weather_current', 'weather_forecast', 'weather_alerts']:
                    actual[param] = actual[param].lower().replace(" ", "_")
                    if str(expected[param]).lower() != str(actual[param]).lower():
                        return False
                else:
                    # Strict matching for other parameters
                    if expected[param] != actual[param]:
                        return False
        return True
    
    def _get_key_params(self, api: str) -> List[str]:
        """Get key parameters that must match for an API"""
        # Simplified approach: Define only complex APIs with optional parameters
        # For most APIs, empty list means validate all parameters
        complex_apis = {
            # APIs with optional parameters - only validate core parameters
            'brightness_adjust': ['endpoints'],  # brightness or direction optional
            'volume_adjust': ['endpoints'],      # volume or direction optional
            
            # APIs with either/or parameters - don't enforce specific parameters
            'get_group_devices': [],            # group_id or group_name either one
            'get_user_inventory': [],           # user_id optional
            'get_messages': [],                 # limit parameter is flexible
            # Transaction APIs
            'add_to_cart': ['product_id'],
            'remove_from_cart': ['product_id'],
            'update_cart_quantity': ['product_id', 'quantity'],
            'track_order': ['order_id'],
            'get_order_history': ['user_id'],
            'cancel_order': ['order_id'],
            
            # Communication APIs
            'make_call': ['phone_number'],
            'send_message': ['recipient', 'message'],
            'get_call_history': ['time_range'],
            
            # Information APIs
            'stock_price': ['symbol'],
            'weather_current': ['location'],
            'weather_forecast': ['location'],
            'knowledge_lookup': ['keyword'],
            'news_by_category': ['category'],
            'weather_alerts': ['location'],
            
            # Supporting queries
            'search_product': ['query'],
            'get_recipe_details': ['recipe_id'],
            'search_recipes': ['query'],
            
            # Culinary APIs
            'save_favorite_recipe': ['recipe_id'],
            'place_delivery_order': ['restaurant_id', 'items', 'delivery_address'],
            'track_delivery_order': ['order_id'],
            'get_restaurant_menu': ['restaurant_id'],
            'view_delivery_order': ['order_id'],
            
            # Media APIs
            'play': ['endpoints', 'media_id'],
            'set_playback_speed': ['endpoints', 'speed'],
            'get_media_details': ['media_id'],
            'add_to_playlist': ['playlist_id', 'media_ids'],
            'create_playlist': ['title'],
        }
        
        return complex_apis.get(api, [])  # Empty list = validate all parameters


@dataclass
class ValidationResult:
    """Unified validation result"""
    success: bool
    missing_side_effects: List[str] = field(default_factory=list)
    incorrect_side_effects: List[str] = field(default_factory=list)
    extra_side_effects: List[str] = field(default_factory=list)
    missing_core_queries: List[str] = field(default_factory=list)
    supporting_query_warnings: List[str] = field(default_factory=list)
    query_warnings: List[str] = field(default_factory=list)  # Keep for backward compatibility
    invalid_api_calls: List[str] = field(default_factory=list)  # New field for invalid API calls
    special_case_results: Dict[str, Any] = field(default_factory=dict)
    failure_reason: str = ""


@dataclass
class TurnAnalysis:
    """Analysis result for a single turn"""
    turn_number: int
    query: str
    validation_result: ValidationResult
    expected_apis: List[UnifiedAPICall]
    actual_apis: List[UnifiedAPICall]
    api_counts: Dict[str, Dict[str, int]]  # {expected: {api: count}, actual: {api: count}}


@dataclass
class ConversationAnalysis:
    """Complete analysis for one conversation"""
    filename: str
    user_id: str
    domain: str
    total_turns: int
    successful_turns: int
    turn_success_rate: float
    conversation_success: bool  # All turns must pass
    turn_analyses: List[TurnAnalysis]
    total_side_effect_errors: int
    total_query_warnings: int
    special_case_summary: Dict[str, Any]


class APIClassifier:
    """Classifies APIs into side-effect, core query, and supporting query categories"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.side_effect_apis = set()
        self.core_query_apis = set()
        self.supporting_query_apis = set()
        self.order_independent_apis = set()
        self.domain_mapping = {}
        
        if config_path and os.path.exists(config_path):
            self._load_config(config_path)
        else:
            self._load_default_config()
    
    def _load_default_config(self):
        """Load default API classification"""
        # Force loading from configuration files
        # If no config provided, this should not be used
        self.side_effect_apis = set()
        self.core_query_apis = set()
        self.supporting_query_apis = set()
        self.order_independent_apis = set()
        self.domain_mapping = {}
        self.non_side_effect_apis = set()
    
    def _load_config(self, config_path: str):
        """Load API classification from YAML config"""
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Load side-effect APIs
        if 'side_effect_apis' in config:
            for domain, apis in config['side_effect_apis'].items():
                self.side_effect_apis.update(apis)
                for api in apis:
                    self.domain_mapping[api] = domain
        
        # Load core query APIs
        if 'core_queries' in config:
            for domain, apis in config['core_queries'].items():
                self.core_query_apis.update(apis)
                for api in apis:
                    self.domain_mapping[api] = domain
        
        # Load supporting query APIs
        if 'supporting_queries' in config:
            for domain, apis in config['supporting_queries'].items():
                self.supporting_query_apis.update(apis)
                for api in apis:
                    self.domain_mapping[api] = domain
        
        # Load order-independent APIs
        if 'order_independent_apis' in config:
            self.order_independent_apis.update(config['order_independent_apis'])
        
        # Update the legacy non_side_effect_apis set for backward compatibility
        self.non_side_effect_apis = self.core_query_apis | self.supporting_query_apis
    
    def is_side_effect_api(self, api_name: str) -> bool:
        """Check if API has side effects"""
        return api_name in self.side_effect_apis
    
    def is_core_query_api(self, api_name: str) -> bool:
        """Check if API is a core query (missing causes failure)"""
        return api_name in self.core_query_apis
    
    def is_supporting_query_api(self, api_name: str) -> bool:
        """Check if API is a supporting query (missing causes warning only)"""
        return api_name in self.supporting_query_apis
    
    def is_order_independent_api(self, api_name: str) -> bool:
        """Check if API is order-independent (can be called in any order)"""
        return api_name in self.order_independent_apis
    
    def classify_api(self, api_name: str) -> str:
        """Classify API as 'side_effect', 'core_query', 'supporting_query', or 'unknown'"""
        if self.is_side_effect_api(api_name):
            return 'side_effect'
        elif self.is_core_query_api(api_name):
            return 'core_query'
        elif self.is_supporting_query_api(api_name):
            return 'supporting_query'
        else:
            return 'unknown'
    
    def get_domain(self, api_name: str) -> str:
        """Get domain for an API"""
        return self.domain_mapping.get(api_name, 'unknown')


class SpecialCaseHandler:
    """Handles domain-specific special cases"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.special_cases = {}
        
        if config_path and os.path.exists(config_path):
            self._load_config(config_path)
        else:
            self._load_default_cases()
    
    def _load_default_cases(self):
        """Load default special cases"""
        self.special_cases = {
            'checkout_required': {
                'description': 'Transaction APIs require checkout',
                'trigger_apis': ['add_to_cart'],
                'require_apis': ['checkout'],
                'domains': ['transaction']
            },
            'strict_param_match': {
                'description': 'APIs requiring strict parameter matching',
                'apis': ['add_to_cart', 'remove_from_cart', 'color_set', 'make_call'],
                'params': ['product_id', 'color', 'phone_number']
            }
        }
    
    def _load_config(self, config_path: str):
        """Load special cases from YAML config"""
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        if 'special_cases' in config:
            self.special_cases = config['special_cases']
    
    def check_special_cases(self, expected_apis: List[UnifiedAPICall], 
                          actual_apis: List[UnifiedAPICall]) -> Dict[str, Any]:
        """Check all special cases and return results"""
        results = {}
        
        # Check checkout requirement
        if 'checkout_required' in self.special_cases:
            results['checkout_required'] = self._check_checkout_requirement(
                expected_apis, actual_apis
            )
        
        return results
    
    def _check_checkout_requirement(self, expected_apis: List[UnifiedAPICall], 
                                  actual_apis: List[UnifiedAPICall]) -> bool:
        """Check if checkout is present when add_to_cart is used"""
        case = self.special_cases['checkout_required']
        
        # Check if trigger APIs are in expected
        has_trigger = any(api.api in case['trigger_apis'] for api in expected_apis)
        
        if has_trigger:
            # Check if required APIs are in actual
            has_required = any(api.api in case['require_apis'] for api in actual_apis)
            return has_required
        
        return True  # No trigger, so requirement is met


class UnifiedValidator:
    """Unified validator with side-effect based validation"""
    
    def __init__(self, config_dir: Optional[str] = None, ad_hoc_mode: bool = False):
        self.classifier = APIClassifier(
            os.path.join(config_dir, 'api_classification.yaml') if config_dir else None
        )
        self.special_handler = SpecialCaseHandler(
            os.path.join(config_dir, 'special_cases.yaml') if config_dir else None
        )
        self.ad_hoc_mode = ad_hoc_mode
        self.api_error_count = {}  # Track errors across conversation
        
        # Ad-hoc APIs (APIs that may fail due to external factors)
        self.ad_hoc_apis = {
            'make_call',
            'get_call_history', 'play', 'color_set', 'lock_lock','lock_unlock',
            'stock_price', 'track_order'
        }
    
    def validate_turn(self, expected_apis: List[Dict], actual_apis: List[Dict], steps_data: Optional[List[Dict]] = None) -> ValidationResult:
        """Validate a single turn with unified logic"""
        
        # Convert to UnifiedAPICall objects
        expected_calls = self._convert_to_unified_calls(expected_apis)
        actual_calls = self._convert_to_unified_calls(actual_apis)
        
        # Separate by type
        expected_side_effects = [api for api in expected_calls if api.is_side_effect]
        expected_queries = [api for api in expected_calls if not api.is_side_effect]
        
        actual_side_effects = [api for api in actual_calls if api.is_side_effect]
        actual_queries = [api for api in actual_calls if not api.is_side_effect]
        
        # Initialize result
        result = ValidationResult(success=True)
        
        # 1. Validate side-effect APIs (strict)
        self._validate_side_effects(
            expected_side_effects, actual_side_effects, result
        )
        
        # 2. Validate query APIs (lenient)
        self._validate_queries(
            expected_queries, actual_queries, result
        )
        
        # 3. Apply ad-hoc rules if enabled
        if self.ad_hoc_mode:
            self._apply_ad_hoc_rules_with_consecutive_failures(
                expected_calls, actual_calls, steps_data, result
            )
        
        # 4. Check special cases
        special_results = self.special_handler.check_special_cases(
            expected_calls, actual_calls
        )
        result.special_case_results = special_results
        
        # 5. Determine overall success
        result.success = self._determine_success(result)
        
        # 6. Generate failure reason
        if not result.success:
            result.failure_reason = self._generate_failure_reason(result)
        
        return result
    
    def _convert_to_unified_calls(self, api_list: List[Dict]) -> List[UnifiedAPICall]:
        """Convert API dictionaries to UnifiedAPICall objects"""
        calls = []
        for api_dict in api_list:
            api_name = api_dict.get('api', '')
            call = UnifiedAPICall(
                api=api_name,
                params=api_dict.get('params', {}),
                is_side_effect=self.classifier.is_side_effect_api(api_name),
                domain=self.classifier.get_domain(api_name)
            )
            calls.append(call)
        return calls
    
    def _validate_side_effects(self, expected: List[UnifiedAPICall], 
                             actual: List[UnifiedAPICall], 
                             result: ValidationResult):
        """Validate side-effect APIs with order-independent support"""
        
        # Separate order-dependent and order-independent APIs
        expected_order_dependent = []
        expected_order_independent = []
        actual_order_dependent = []
        actual_order_independent = []
        
        for api in expected:
            if self.classifier.is_order_independent_api(api.api):
                expected_order_independent.append(api)
            else:
                expected_order_dependent.append(api)
        
        for api in actual:
            if self.classifier.is_order_independent_api(api.api):
                actual_order_independent.append(api)
            else:
                actual_order_dependent.append(api)
        
        # Validate order-independent APIs using set-based matching
        self._validate_order_independent_apis(
            expected_order_independent, actual_order_independent, result
        )
        
        # Validate order-dependent APIs using sequence-based matching
        self._validate_order_dependent_apis(
            expected_order_dependent, actual_order_dependent, result
        )
    
    def _validate_order_independent_apis(self, expected: List[UnifiedAPICall], 
                                       actual: List[UnifiedAPICall], 
                                       result: ValidationResult):
        """Validate order-independent APIs using count-based matching"""
        
        # Count expected APIs by (api_name, key_params)
        expected_counts = Counter()
        for api in expected:
            key = self._get_api_signature(api)
            expected_counts[key] += 1
        
        # Count actual APIs by (api_name, key_params)
        actual_counts = Counter()
        for api in actual:
            key = self._get_api_signature(api)
            actual_counts[key] += 1
        
        # Check for missing APIs
        for key, expected_count in expected_counts.items():
            actual_count = actual_counts.get(key, 0)
            if actual_count < expected_count:
                missing_count = expected_count - actual_count
                for _ in range(missing_count):
                    result.missing_side_effects.append(key)  # Store full signature
        
        # Check for extra APIs
        for key, actual_count in actual_counts.items():
            expected_count = expected_counts.get(key, 0)
            if actual_count > expected_count:
                extra_count = actual_count - expected_count
                for _ in range(extra_count):
                    result.extra_side_effects.append(key)  # Store full signature
    
    def _validate_order_dependent_apis(self, expected: List[UnifiedAPICall], 
                                     actual: List[UnifiedAPICall], 
                                     result: ValidationResult):
        """Validate order-dependent APIs with strict sequence matching"""
        
        # For order-dependent APIs, use the original strict matching logic
        expected_matched = [False] * len(expected)
        actual_matched = [False] * len(actual)
        
        # First pass: exact matches with position consideration
        for i, exp_api in enumerate(expected):
            for j, act_api in enumerate(actual):
                if (not actual_matched[j] and 
                    exp_api.matches(act_api, strict_params=True)):
                    expected_matched[i] = True
                    actual_matched[j] = True
                    break
        
        # Check for missing APIs
        for i, matched in enumerate(expected_matched):
            if not matched:
                result.missing_side_effects.append(expected[i].api)
        
        # Check for extra APIs
        for j, matched in enumerate(actual_matched):
            if not matched:
                result.extra_side_effects.append(actual[j].api)
    
    def _get_api_signature(self, api: UnifiedAPICall) -> str:
        """Get API signature for order-independent matching"""
        key_params = api._get_key_params(api.api)
        
        if not key_params:
            return api.api
        
        # Create signature from key parameters
        param_parts = []
        for param in sorted(key_params):  # Sort for consistency
            if param in api.params:
                param_parts.append(f"{param}:{api.params[param]}")
        
        if param_parts:
            return f"{api.api}({','.join(param_parts)})"
        else:
            return api.api
    
    def _validate_queries(self, expected: List[UnifiedAPICall], 
                        actual: List[UnifiedAPICall], 
                        result: ValidationResult):
        """Validate query APIs with two-tier system: core queries vs supporting queries"""
        
        # For each expected query API, find matching actual API
        for exp_api in expected:
            found_match = False
            
            # Look for matching API in actual calls
            for act_api in actual:
                if exp_api.api == act_api.api:
                    if self.classifier.is_core_query_api(exp_api.api):
                        # Core query APIs need strict parameter matching
                        if exp_api.matches(act_api, strict_params=True):
                            found_match = True
                            break
                    else:
                        # Supporting query APIs only need API name matching
                        found_match = True
                        break
            
            # Handle missing APIs
            if not found_match:
                if self.classifier.is_core_query_api(exp_api.api):
                    # Core query missing = failure
                    result.missing_core_queries.append(exp_api.api)
                elif self.classifier.is_supporting_query_api(exp_api.api):
                    # Supporting query missing = warning only
                    result.supporting_query_warnings.append(f"Missing supporting query: {exp_api.api}")
                else:
                    # Fallback to legacy behavior for unknown queries
                    result.query_warnings.append(f"Missing query: {exp_api.api}")
        
        # Update legacy field for backward compatibility
        result.query_warnings.extend(result.supporting_query_warnings)
    
    def _apply_ad_hoc_rules_with_consecutive_failures(self, expected: List[UnifiedAPICall], 
                                                    actual: List[UnifiedAPICall], 
                                                    steps_data: Optional[List[Dict]], 
                                                    result: ValidationResult):
        """Apply ad-hoc rules with consecutive failure detection"""
        
        if not steps_data:
            # Fallback to old behavior if no steps data provided
            print("No Step Data!")
            return
        
        # Check for ad-hoc APIs with consecutive failure patterns
        expected_ad_hoc = [api for api in expected if api.api in self.ad_hoc_apis]
        
        for exp_api in expected_ad_hoc:
            # Find all matching API calls in steps (in order)
            matching_calls = []
            for step in steps_data:
                if (step.get('api_call') and 
                    step['api_call'].get('api') == exp_api.api):
                    matching_calls.append({
                        'api_call': step['api_call'],
                        'success': step.get('api_success', False),
                        'step_number': step.get('step_number', 0)
                    })
            
            if not matching_calls:
                # No matching API calls found - treat as missing
                if exp_api.is_side_effect:
                    result.missing_side_effects.append(exp_api.api)
                else:
                    result.missing_core_queries.append(exp_api.api)
                continue
            
            # Check for consecutive failures
            consecutive_failures = self._count_consecutive_failures(matching_calls)
            
            if consecutive_failures >= 2:
                # Mark as incorrect due to consecutive failures
                result.incorrect_side_effects.append(
                    f"{exp_api.api} (ad-hoc: {consecutive_failures} consecutive failures)"
                )
            else:
                # Check if any call succeeded with correct parameters
                found_correct_match = False
                for call_info in matching_calls:
                    if call_info['success']:
                        # Check if parameters match
                        actual_call = UnifiedAPICall(
                            api=call_info['api_call']['api'],
                            params=call_info['api_call'].get('params', {}),
                            is_side_effect=exp_api.is_side_effect,
                            domain=exp_api.domain
                        )
                        if exp_api.matches(actual_call, strict_params=True):
                            found_correct_match = True
                            break
                
                if not found_correct_match:
                    # No successful call with correct parameters
                    if exp_api.is_side_effect:
                        result.missing_side_effects.append(exp_api.api)
                    else:
                        result.missing_core_queries.append(exp_api.api)
    

    
    def _count_consecutive_failures(self, matching_calls: List[Dict]) -> int:
        """Count the maximum number of consecutive failures from the start"""
        
        if not matching_calls:
            return 0
        
        # Sort by step number to ensure correct order
        sorted_calls = sorted(matching_calls, key=lambda x: x['step_number'])
        
        # Count consecutive failures from the beginning
        consecutive_failures = 0
        for call_info in sorted_calls:
            if not call_info['success']:
                consecutive_failures += 1
            else:
                # Success breaks the consecutive failure chain
                break
        
        return consecutive_failures
    
    def _determine_success(self, result: ValidationResult) -> bool:
        """Determine if validation passed"""
        
        # Check for invalid API calls first (non-existent APIs)
        if len(result.invalid_api_calls) > 0:
            return False
        
        # Basic success: no missing or incorrect side-effects, and no missing core queries
        basic_success = (
            len(result.missing_side_effects) == 0 and
            len(result.incorrect_side_effects) == 0 and
            len(result.missing_core_queries) == 0  # Core queries are mandatory
        )
        
        # Check special cases
        special_success = all(
            result.special_case_results.get(case, True) 
            for case in result.special_case_results
        )
        
        return basic_success and special_success
    
    def _generate_failure_reason(self, result: ValidationResult) -> str:
        """Generate human-readable failure reason"""
        reasons = []
        
        if result.invalid_api_calls:
            reasons.append(f"Invalid API calls (non-existent): {', '.join(result.invalid_api_calls)}")
        
        if result.missing_side_effects:
            reasons.append(f"Missing side-effect APIs: {', '.join(result.missing_side_effects)}")
        
        if result.incorrect_side_effects:
            reasons.append(f"Incorrect side-effect APIs: {', '.join(result.incorrect_side_effects)}")
        
        if result.extra_side_effects:
            reasons.append(f"Extra side-effect APIs: {', '.join(result.extra_side_effects)}")
        
        if result.missing_core_queries:
            reasons.append(f"Missing core queries: {', '.join(result.missing_core_queries)}")
        
        # Check special cases
        for case, passed in result.special_case_results.items():
            if not passed:
                reasons.append(f"Special case failed: {case}")
        
        return "; ".join(reasons)


class UnifiedAnalyzer:
    """Main analyzer using unified validation logic"""
    
    def __init__(self, config_dir: Optional[str] = None, ad_hoc_mode: bool = False):
        self.validator = UnifiedValidator(config_dir, ad_hoc_mode)
        self.ad_hoc_mode = ad_hoc_mode
    
    def analyze_file(self, filepath: str) -> ConversationAnalysis:
        """Analyze a single result file"""
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            raise ValueError(f"Failed to load file {filepath}: {e}")
        
        filename = os.path.basename(filepath)
        user_id = data.get("user_id", "unknown")
        
        # Detect domain from filename
        domain = self._detect_domain(filename)
        
        # Analyze each turn
        query_results = data.get("query_results", [])
        query_results = self._preprocess_expected_apis(query_results)

        turn_analyses = []
        total_side_effect_errors = 0
        total_query_warnings = 0
        
        for i, query_result in enumerate(query_results):
            turn_analysis = self._analyze_turn(query_result, i + 1)
            turn_analyses.append(turn_analysis)
            
            # Count errors
            if not turn_analysis.validation_result.success:
                total_side_effect_errors += (
                    len(turn_analysis.validation_result.missing_side_effects) +
                    len(turn_analysis.validation_result.incorrect_side_effects) +
                    len(turn_analysis.validation_result.extra_side_effects)
                )
            total_query_warnings += len(turn_analysis.validation_result.query_warnings)
        
        # Calculate metrics
        successful_turns = sum(1 for t in turn_analyses if t.validation_result.success)
        turn_success_rate = successful_turns / len(turn_analyses) if turn_analyses else 0.0
        
        # Strict conversation success
        conversation_success = successful_turns == len(turn_analyses) and len(turn_analyses) > 0
        
        # Aggregate special case results
        special_case_summary = defaultdict(int)
        for turn in turn_analyses:
            for case, result in turn.validation_result.special_case_results.items():
                if result:
                    special_case_summary[f"{case}_passed"] += 1
                else:
                    special_case_summary[f"{case}_failed"] += 1
        
        return ConversationAnalysis(
            filename=filename,
            user_id=user_id,
            domain=domain,
            total_turns=len(turn_analyses),
            successful_turns=successful_turns,
            turn_success_rate=turn_success_rate,
            conversation_success=conversation_success,
            turn_analyses=turn_analyses,
            total_side_effect_errors=total_side_effect_errors,
            total_query_warnings=total_query_warnings,
            special_case_summary=dict(special_case_summary)
        )
    
    # ! label issue fix
    def _preprocess_expected_apis(self, query_results: List[Dict]) -> List[Dict]:
        """Preprocess expected APIs to handle special cases"""
        device_states = {}  # Track device power states across turns
        
        for query_result in query_results:
            expected_apis = query_result.get("expected_api_sequence", [])
            
            # Case 1: Remove lock_lock with endpoint 29
            expected_apis = [api for api in expected_apis 
                           if not (api.get('api') == 'lock_lock' and 
                                  '29' in str(api.get('params', {}).get('endpoints', [])))]
            
            # # Case 2: Handle power_on duplicates
            # expected_apis = self._handle_power_on_duplicates(expected_apis, device_states)
            
            # # Update device states
            # self._update_device_states(expected_apis, device_states)

            # ! label issue resolve for Conv_user5_scenario8_investment_check_MultiTool_NotificationCall_merged.jsonl & Conv_user5_scenario7_business_day_MultiTool_NotificationCall_merged.jsonl
            if expected_apis == [{"api": "find_contact", "params": {"query": "Jessica Carter", "search_type": "name", "limit": 1}}, {"api": "find_call_device", "params": {}}, {"api": "power_on", "params": {"endpoints": ["17"]}}, {"api": "make_call", "params": {"phone_number": "D:4157863264", "call_type": "audio", "device_endpoint": "17"}}]:
                expected_apis = [{"api": "find_contact", "params": {"query": "Jessica Carter", "search_type": "name", "limit": 1}}, {"api": "find_call_device", "params": {}}, {"api": "make_call", "params": {"phone_number": "D:4157863264", "call_type": "audio", "device_endpoint": "17"}}]

            query_result["expected_api_sequence"] = expected_apis
        
        return query_results
    def _detect_domain(self, filename: str) -> str:
        """Detect domain from filename patterns"""
        patterns = {
            'transaction': ['transaction', 'shopping', 'cart', 'checkout'],
            'smarthome': ['smarthome', 'device', 'lock', 'light'],
            'communication': ['call', 'message', 'contact'],
            'culinary': ['culinary', 'recipe', 'ingredient'],
            'investment': ['investment', 'stock', 'portfolio'],
            'brand_reference': ['brand_reference', 'brand'],
            'color_reference': ['color_reference', 'color'],
        }
        
        filename_lower = filename.lower()
        for domain, keywords in patterns.items():
            if any(keyword in filename_lower for keyword in keywords):
                return domain
        
        return 'unknown'
    
    def _analyze_turn(self, query_result: Dict, turn_number: int) -> TurnAnalysis:
        """Analyze a single turn"""
        
        query = query_result.get("query", "")
        expected_api_sequence = query_result.get("expected_api_sequence", [])
        steps = query_result.get("steps", [])
        
        # Extract actual API calls and detect invalid APIs
        actual_apis = []
        invalid_apis = []
        
        for step in steps:
            api_call = step.get("api_call")
            if api_call:
                api_name = api_call.get('api', '')
                api_result = step.get('api_result', '')
                
                # Check for invalid API calls (API doesn't exist)
                if ("not found in any environment" in api_result or 
                    ("Tool" in api_result and "not found" in api_result)):
                    invalid_apis.append(api_name)
                    continue  # Skip this API call - don't include in actual_apis
                
                is_side_effect = self.validator.classifier.is_side_effect_api(api_name)
                
                if is_side_effect:
                    # Side-effect APIs: only successful calls count (produce actual effects)
                    if step.get('api_success', False):
                        actual_apis.append(api_call)
                else:
                    # Non-side-effect APIs: all calls count (queries don't need success check)
                    actual_apis.append(api_call)
        
        # Validate with steps data for ad-hoc consecutive failure detection
        validation_result = self.validator.validate_turn(
            expected_api_sequence, actual_apis, steps
        )
        
        # Add invalid API calls to validation result
        validation_result.invalid_api_calls.extend(invalid_apis)
        
        # Re-evaluate success after adding invalid API calls
        if len(validation_result.invalid_api_calls) > 0:
            validation_result.success = False
            # Regenerate failure reason to include invalid APIs
            validation_result.failure_reason = self.validator._generate_failure_reason(validation_result)
        
        # Convert to unified calls for analysis
        expected_calls = self.validator._convert_to_unified_calls(expected_api_sequence)
        actual_calls = self.validator._convert_to_unified_calls(actual_apis)
        
        # Count APIs
        expected_counts = Counter(call.api for call in expected_calls)
        actual_counts = Counter(call.api for call in actual_calls)
        
        return TurnAnalysis(
            turn_number=turn_number,
            query=query,
            validation_result=validation_result,
            expected_apis=expected_calls,
            actual_apis=actual_calls,
            api_counts={
                'expected': dict(expected_counts),
                'actual': dict(actual_counts)
            }
        )


class UnifiedReporter:
    """Generates unified reports"""
    
    def generate_single_report(self, analysis: ConversationAnalysis) -> str:
        """Generate report for single conversation"""
        
        lines = []
        lines.append("=" * 80)
        lines.append(f"UNIFIED ANALYSIS: {analysis.filename}")
        lines.append("=" * 80)
        lines.append("")
        
        # Summary
        status = "✅ PASS" if analysis.conversation_success else "❌ FAIL"
        lines.append("📊 SUMMARY")
        lines.append(f"   File: {analysis.filename}")
        lines.append(f"   User: {analysis.user_id}")
        lines.append(f"   Domain: {analysis.domain}")
        lines.append(f"   Status: {status}")
        lines.append(f"   Total Turns: {analysis.total_turns}")
        lines.append(f"   Successful Turns: {analysis.successful_turns}")
        lines.append(f"   Turn Success Rate: {analysis.turn_success_rate:.1%}")
        lines.append("")
        
        # Error Summary
        if analysis.total_side_effect_errors > 0 or analysis.total_query_warnings > 0:
            lines.append("⚠️ ERROR SUMMARY")
            lines.append(f"   Side-Effect Errors: {analysis.total_side_effect_errors}")
            lines.append(f"   Query Warnings: {analysis.total_query_warnings}")
            lines.append("")
        
        # Special Cases
        if analysis.special_case_summary:
            lines.append("🔍 SPECIAL CASES")
            for case, count in analysis.special_case_summary.items():
                lines.append(f"   {case}: {count}")
            lines.append("")
        
        # Turn-by-Turn Analysis
        lines.append("📋 TURN-BY-TURN ANALYSIS")
        for turn in analysis.turn_analyses:
            result = turn.validation_result
            status_icon = "✅" if result.success else "❌"
            
            lines.append(f"   Turn {turn.turn_number}: {status_icon}")
            lines.append(f"   Query: {turn.query}")
            
            # Expected workflow
            if turn.expected_apis:
                lines.append("   Expected:")
                for api in turn.expected_apis:
                    type_icon = "🔄" if api.is_side_effect else "🔍"
                    params_str = json.dumps(api.params, separators=(',', ':'))
                    lines.append(f"     {type_icon} {api.api}({params_str})")
            
            # Actual workflow
            if turn.actual_apis:
                lines.append("   Actual:")
                for api in turn.actual_apis:
                    type_icon = "🔄" if api.is_side_effect else "🔍"
                    params_str = json.dumps(api.params, separators=(',', ':'))
                    lines.append(f"     {type_icon} {api.api}({params_str})")
            
            # Errors
            if not result.success:
                lines.append(f"   Failure: {result.failure_reason}")
                
                if result.missing_side_effects:
                    lines.append(f"   Missing Side-Effects: {', '.join(result.missing_side_effects)}")
                if result.incorrect_side_effects:
                    lines.append(f"   Incorrect Side-Effects: {', '.join(result.incorrect_side_effects)}")
                if result.extra_side_effects:
                    lines.append(f"   Extra Side-Effects: {', '.join(result.extra_side_effects)}")
                if result.missing_core_queries:
                    lines.append(f"   Missing Core Queries: {', '.join(result.missing_core_queries)}")
                if result.supporting_query_warnings:
                    lines.append(f"   Supporting Query Warnings: {', '.join(result.supporting_query_warnings)}")
            
            lines.append("")
        
        return "\n".join(lines)
    
    def generate_batch_summary(self, analyses: List[ConversationAnalysis]) -> str:
        """Generate batch summary report"""
        
        if not analyses:
            return "No files analyzed."
        
        lines = []
        lines.append("=" * 80)
        lines.append("UNIFIED BATCH ANALYSIS SUMMARY")
        lines.append("=" * 80)
        lines.append("")
        
        # Overall Statistics
        total_files = len(analyses)
        successful_files = sum(1 for a in analyses if a.conversation_success)
        success_rate = successful_files / total_files
        
        # Calculate turn-level statistics across all conversations
        total_turns = sum(a.total_turns for a in analyses)
        total_successful_turns = sum(a.successful_turns for a in analyses)
        turn_success_rate = total_successful_turns / total_turns if total_turns > 0 else 0
        
        lines.append("📊 OVERALL STATISTICS")
        lines.append(f"   Total Files: {total_files}")
        lines.append(f"   Successful: {successful_files}")
        lines.append(f"   Success Rate: {success_rate:.1%}")
        lines.append(f"   Turn-Level Success Rate: {turn_success_rate:.1%} ({total_successful_turns}/{total_turns})")
        lines.append("")
        
        # Domain Breakdown
        domain_stats = defaultdict(lambda: {'total': 0, 'successful': 0})
        for analysis in analyses:
            domain_stats[analysis.domain]['total'] += 1
            if analysis.conversation_success:
                domain_stats[analysis.domain]['successful'] += 1
        
        lines.append("🌐 DOMAIN BREAKDOWN")
        for domain, stats in sorted(domain_stats.items()):
            rate = stats['successful'] / stats['total'] if stats['total'] > 0 else 0
            lines.append(f"   {domain}: {stats['successful']}/{stats['total']} ({rate:.1%})")
        lines.append("")
        
        # File Summary
        lines.append("📁 FILE SUMMARY")
        for analysis in analyses:
            status = "✅" if analysis.conversation_success else "❌"
            lines.append(f"   {status} {analysis.filename}")
            lines.append(f"      Domain: {analysis.domain}")
            lines.append(f"      Turn Success Rate: {analysis.turn_success_rate:.1%} ({analysis.successful_turns}/{analysis.total_turns})")
            
            # Show error details for failed conversations
            if not analysis.conversation_success:
                failed_turns = [turn for turn in analysis.turn_analyses if not turn.validation_result.success]
                if failed_turns:
                    lines.append(f"      Failed Turns ({len(failed_turns)}):")
                    
                    # Show all failed turns
                    for turn in failed_turns:
                        query_preview = turn.query
                        lines.append(f"        Turn {turn.turn_number}: {query_preview}")
                        
                        # Expected workflow
                        if turn.expected_apis:
                            expected_flow_parts = []
                            for api in turn.expected_apis:
                                params_str = json.dumps(api.params, separators=(',', ':'))
                                expected_flow_parts.append(f"{api.api}({params_str})")
                            expected_flow = " → ".join(expected_flow_parts)
                            lines.append(f"        Expected: {expected_flow}")
                        
                        # Actual workflow
                        if turn.actual_apis:
                            actual_flow_parts = []
                            for api in turn.actual_apis:
                                params_str = json.dumps(api.params, separators=(',', ':'))
                                actual_flow_parts.append(f"{api.api}({params_str})")
                            actual_flow = " → ".join(actual_flow_parts)
                            lines.append(f"        Actual: {actual_flow}")
                        
                        lines.append(f"        └── {turn.validation_result.failure_reason}")
            
            lines.append("")
        
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Unified Analyzer for conversation test results",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Analyze single file
    python unified_analyzer.py result.json
    
    # Batch analyze directory
    python unified_analyzer.py test_results/ --batch
    
    # Batch analyze with ad-hoc mode
    python unified_analyzer.py test_results/ --batch --ad_hoc
    
    # Use custom configuration
    python unified_analyzer.py result.json --config configs/
        """
    )
    
    parser.add_argument("input", help="Input file or directory")
    parser.add_argument("--batch", action="store_true", help="Batch process directory")
    parser.add_argument("--config", help="Configuration directory")
    parser.add_argument("--ad_hoc", action="store_true", help="Enable ad-hoc mode")
    parser.add_argument("--output", "-o", help="Output directory for reports")
    
    args = parser.parse_args()
    
    try:
        # Set default config directory if not provided
        config_dir = args.config or "configs"
        
        # Create analyzer
        analyzer = UnifiedAnalyzer(
            config_dir=config_dir,
            ad_hoc_mode=args.ad_hoc
        )
        reporter = UnifiedReporter()
        
        if args.batch:
            # Batch processing
            input_path = Path(args.input)
            if not input_path.exists():
                raise ValueError(f"Directory does not exist: {args.input}")
            
            # Find all JSON result files
            json_files = list(input_path.glob("*_test_result.json"))
            if not json_files:
                json_files = list(input_path.glob("*.json"))
            if not json_files:
                print(f"No *_test_result.json files found in {args.input}")
                return
            
            print(f"Found {len(json_files)} files to analyze...")
            
            # Analyze each file
            analyses = []
            for json_file in sorted(json_files):
                try:
                    print(f"Analyzing {json_file.name}...")
                    analysis = analyzer.analyze_file(str(json_file))
                    analyses.append(analysis)
                    
                    # Save individual report if output specified
                    if args.output:
                        output_path = Path(args.output)
                        output_path.mkdir(exist_ok=True)
                        
                        report_filename = json_file.stem
                        if report_filename.endswith("_test_result"):
                            report_filename = report_filename.replace("_test_result", "_unified_analysis.txt")
                        else:
                            report_filename = f"{report_filename}_unified_analysis.txt"   
                        report_path = output_path / report_filename
                        
                        report = reporter.generate_single_report(analysis)
                        with open(report_path, 'w', encoding='utf-8') as f:
                            f.write(report)
                        print(f"  → Report saved: {report_path}")
                
                except Exception as e:
                    print(f"  ❌ Error analyzing {json_file.name}: {e}")
            
            # Generate and display batch summary
            if analyses:
                summary = reporter.generate_batch_summary(analyses)
                print("\n" + summary)
                
                # Save batch summary if output specified
                if args.output:
                    summary_path = Path(args.output) / "unified_batch_summary.txt"
                    with open(summary_path, 'w', encoding='utf-8') as f:
                        f.write(summary)
                    print(f"\n📋 Batch summary saved: {summary_path}")
        
        else:
            # Single file processing
            analysis = analyzer.analyze_file(args.input)
            report = reporter.generate_single_report(analysis)
            
            print(report)
            
            # Save report if output specified
            if args.output:
                output_path = Path(args.output)
                output_path.mkdir(exist_ok=True)
                
                filename = Path(args.input).stem
                print(filename)
                if filename.endswith("_test_result"):
                    filename = filename.replace("_test_result", "_unified_analysis.txt")
                else:
                    filename = f"{filename}_unified_analysis.txt"    

                report_path = output_path / filename
                with open(report_path, 'w', encoding='utf-8') as f:
                    f.write(report)
                print(f"\n📋 Report saved: {report_path}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

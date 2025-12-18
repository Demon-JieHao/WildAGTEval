#!/usr/bin/env python3
"""
Uncertainty Manager for Step-by-Step LLM Evaluator

This module manages uncertainty configurations and applies them during API calls.
"""

import yaml
import os
from contextlib import contextmanager
from typing import Dict, List, Set, Tuple
from pathlib import Path


class UncertaintyManager:
    """
    Manages uncertainty configurations and applies them during API execution.
    
    Based on UNCERTAINTY_ENVIRONMENT_VARIABLES.md:
    - 24 total uncertainty environment variables
    - 3 uncertainty types: FEATURE_LIMITATION_ERROR, PARTIALLY_IRRELEVANT_INFORMATION, INFORMATIONAL_NOTICE
    - Some APIs have multiple uncertainty types
    """
    
    def __init__(self, config_path: str):
        """
        Initialize uncertainty manager with YAML configuration.
        
        Args:
            config_path: Path to YAML configuration file
        """
        self.config_path = config_path
        self.config = self.load_config(config_path)
        self.api_to_env_mapping = self.build_api_mapping()
        self.uncertainty_stats = self.calculate_stats()
        
    def load_config(self, config_path: str) -> Dict:
        """Load uncertainty configuration from YAML file."""
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Uncertainty config file not found: {config_path}")
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Validate configuration structure
        if 'uncertainties' not in config:
            raise ValueError("Config must contain 'uncertainties' section")
        
        # Flexible validation - just ensure uncertainties section has content
        if not config['uncertainties']:
            raise ValueError("Config 'uncertainties' section cannot be empty")
        
        return config
    
    def build_api_mapping(self) -> Dict[str, List[Tuple[str, str]]]:
        """
        Build mapping from API names to their uncertainty environment variables.
        
        Returns:
            Dict mapping API name to list of (env_var, uncertainty_type) tuples
        """
        mapping = {}
        
        for uncertainty_type, type_config in self.config['uncertainties'].items():
            if not type_config.get('enabled', False):
                continue
                
            apis = type_config.get('apis', [])
            for api in apis:
                if api not in mapping:
                    mapping[api] = []
                
                # Convert API name to environment variable format
                env_var = f"ENABLE__{uncertainty_type}__{api.upper()}"
                mapping[api].append((env_var, uncertainty_type))
        
        return mapping
    
    def calculate_stats(self) -> Dict:
        """Calculate statistics about active uncertainties."""
        # Dynamically get all uncertainty types from the config
        uncertainty_types = list(self.config['uncertainties'].keys())
        
        stats = {
            'total_apis_with_uncertainties': len(self.api_to_env_mapping),
            'total_active_env_vars': 0,
            'uncertainty_type_counts': {utype: 0 for utype in uncertainty_types},
            'apis_by_uncertainty_type': {utype: [] for utype in uncertainty_types}
        }
        
        for api, env_vars in self.api_to_env_mapping.items():
            stats['total_active_env_vars'] += len(env_vars)
            
            for env_var, uncertainty_type in env_vars:
                stats['uncertainty_type_counts'][uncertainty_type] += 1
                stats['apis_by_uncertainty_type'][uncertainty_type].append(api)
        
        return stats
    
    def get_env_vars_for_api(self, api_name: str) -> List[Tuple[str, str]]:
        """
        Get environment variables and their types for a specific API.
        
        Args:
            api_name: Name of the API
            
        Returns:
            List of (env_var, uncertainty_type) tuples
        """
        return self.api_to_env_mapping.get(api_name, [])
    
    def get_uncertainty_types_for_api(self, api_name: str) -> List[str]:
        """Get list of uncertainty types active for an API."""
        return [uncertainty_type for _, uncertainty_type in self.get_env_vars_for_api(api_name)]
    
    def has_uncertainties_for_api(self, api_name: str) -> bool:
        """Check if API has any active uncertainties."""
        return len(self.get_env_vars_for_api(api_name)) > 0
    
    @contextmanager
    def apply_uncertainties_for_api(self, api_name: str):
        """
        Apply uncertainties for a specific API call.
        
        Args:
            api_name: Name of the API being called
            
        Yields:
            Dict with applied uncertainty information
        """
        env_vars_and_types = self.get_env_vars_for_api(api_name)
        
        if not env_vars_and_types:
            # No uncertainties for this API
            yield {
                'api_name': api_name,
                'applied_uncertainties': [],
                'uncertainty_types': [],
                'has_uncertainties': False
            }
            return
        
        # Extract environment variables and types
        env_vars = [env_var for env_var, _ in env_vars_and_types]
        uncertainty_types = [uncertainty_type for _, uncertainty_type in env_vars_and_types]
        
        # Backup original environment variable values
        original_values = {}
        for env_var in env_vars:
            original_values[env_var] = os.environ.get(env_var)
            os.environ[env_var] = 'true'
        
        try:
            yield {
                'api_name': api_name,
                'applied_uncertainties': env_vars,
                'uncertainty_types': uncertainty_types,
                'has_uncertainties': True
            }
        finally:
            # Restore original environment variable values
            for env_var in env_vars:
                if original_values[env_var] is None:
                    os.environ.pop(env_var, None)
                else:
                    os.environ[env_var] = original_values[env_var]
    
    def get_config_summary(self) -> Dict:
        """Get summary of current configuration."""
        return {
            'config_name': self.config.get('name', 'Unknown'),
            'config_description': self.config.get('description', 'No description'),
            'config_path': self.config_path,
            'statistics': self.uncertainty_stats,
            'enabled_uncertainty_types': [
                uncertainty_type for uncertainty_type, type_config in self.config['uncertainties'].items()
                if type_config.get('enabled', False)
            ]
        }
    
    def print_config_info(self):
        """Print configuration information for debugging."""
        summary = self.get_config_summary()
        
        print(f"🎯 Uncertainty Configuration: {summary['config_name']}")
        print(f"📝 Description: {summary['config_description']}")
        print(f"📁 Config Path: {summary['config_path']}")
        print(f"\n📊 Statistics:")
        print(f"   Total APIs with uncertainties: {summary['statistics']['total_apis_with_uncertainties']}")
        print(f"   Total active environment variables: {summary['statistics']['total_active_env_vars']}")
        
        print(f"\n🔧 Enabled Uncertainty Types:")
        for uncertainty_type in summary['enabled_uncertainty_types']:
            count = summary['statistics']['uncertainty_type_counts'][uncertainty_type]
            apis = summary['statistics']['apis_by_uncertainty_type'][uncertainty_type]
            print(f"   {uncertainty_type}: {count} APIs")
            if apis:
                print(f"      APIs: {', '.join(apis)}")
    
    @staticmethod
    def create_empty_config() -> Dict:
        """Create an empty uncertainty configuration."""
        return {
            'name': 'No Uncertainties',
            'description': 'Clean evaluation without any uncertainties',
            'uncertainties': {
                'FEATURE_LIMITATION_ERROR': {
                    'enabled': False,
                    'apis': []
                },
                'PARTIALLY_IRRELEVANT_INFORMATION': {
                    'enabled': False,
                    'apis': []
                },
                'INFORMATIONAL_NOTICE': {
                    'enabled': False,
                    'apis': []
                }
            }
        }


def create_uncertainty_config_directory():
    """Create uncertainty_configs directory with sample configurations."""
    config_dir = Path("uncertainty_configs")
    config_dir.mkdir(exist_ok=True)
    
    return config_dir


if __name__ == "__main__":
    """
    Test the UncertaintyManager with sample configurations.
    """
    # This is for testing purposes only
    print("🧪 Testing UncertaintyManager...")
    
    # Create a sample config for testing
    sample_config = {
        'name': 'Test Configuration',
        'description': 'Sample configuration for testing',
        'uncertainties': {
            'FEATURE_LIMITATION_ERROR': {
                'enabled': True,
                'apis': ['get_call_history', 'get_messages']
            },
            'PARTIALLY_IRRELEVANT_INFORMATION': {
                'enabled': True,
                'apis': ['search_recipes', 'get_call_history']
            },
            'INFORMATIONAL_NOTICE': {
                'enabled': False,
                'apis': []
            }
        }
    }
    
    # Write sample config to temporary file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(sample_config, f)
        temp_config_path = f.name
    
    try:
        # Test UncertaintyManager
        manager = UncertaintyManager(temp_config_path)
        manager.print_config_info()
        
        print(f"\n🔍 Testing API uncertainty lookup...")
        test_apis = ['get_call_history', 'search_recipes', 'power_on']
        
        for api in test_apis:
            env_vars = manager.get_env_vars_for_api(api)
            uncertainty_types = manager.get_uncertainty_types_for_api(api)
            has_uncertainties = manager.has_uncertainties_for_api(api)
            
            print(f"   {api}: {has_uncertainties}")
            if has_uncertainties:
                print(f"      Types: {uncertainty_types}")
                print(f"      Env vars: {[env for env, _ in env_vars]}")
        
        # Test context manager
        print(f"\n🧪 Testing uncertainty application...")
        with manager.apply_uncertainties_for_api('get_call_history') as uncertainty_info:
            print(f"   Applied uncertainties: {uncertainty_info}")
            
        print(f"\n✅ UncertaintyManager test completed successfully!")
        
    finally:
        # Clean up temporary file
        os.unlink(temp_config_path)

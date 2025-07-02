"""
Configuration management for GitHub Profile Generator
Handles loading and validation of user configuration from JSON file
"""

import json
import os
from typing import Dict, Any
from .utils import auto_detect_environment


class ConfigManager:
    """Manages configuration loading and validation"""
    
    DEFAULT_CONFIG = {
        "environment": {
            "os": "macOS Sequoia",
            "version": "15.5 (24F74)",
            "editor": "VS Code (1.100.2)"
        },
        "packaging_languages": {
            "languages": ["TypeScript", "Python", "Go", "React"]
        },
        "server_region": {
            "region": "Europe/London"
        },
        "host": {
            "platform": "Marketplace Platforms"
        },
        "social": {
            "linkedin": "linkedin.com/lewiselborn",
            "twitter": "twitter.com/lelborn",
            "website": "lewiselborn.com",
            "email": "lewis@lewiselborn.com"
        }
    }
    
    def __init__(self, config_path: str = "profile_config.json"):
        """Initialize configuration manager"""
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file or use defaults"""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                print(f"✅ Configuration loaded from {self.config_path}")
                return config
        except FileNotFoundError:
            print(f"⚠️  {self.config_path} not found, using default configuration")
            return self.DEFAULT_CONFIG
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing {self.config_path}: {e}")
            print("Using default configuration")
            return self.DEFAULT_CONFIG
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation (e.g., 'environment.os')"""
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def merge_github_data(self, github_data: Dict[str, Any]) -> None:
        """Merge GitHub API data with configuration, prioritizing GitHub data"""
        if not github_data:
            return
        
        # Update social section with GitHub data
        if 'social' not in self.config:
            self.config['social'] = {}
        
        social = self.config['social']
        
        # Update social links from GitHub data (only if not already set)
        if github_data.get('website') and ('website' not in social or not social['website']):
            social['website'] = github_data['website']
        if github_data.get('twitter') and ('twitter' not in social or not social['twitter']):
            social['twitter'] = f"twitter.com/{github_data['twitter']}"
        if github_data.get('email') and ('email' not in social or not social['email']):
            social['email'] = github_data['email']
        
        print("✅ GitHub data merged with configuration")
    
    def get_merged_config(self, github_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get configuration with GitHub data merged in"""
        if github_data:
            self.merge_github_data(github_data)
        return self.config
    
    def get_environment_info(self) -> Dict[str, Any]:
        """Get environment information section"""
        return self.config.get('environment', {})
    
    def get_packaging_languages(self) -> Dict[str, Any]:
        """Get packaging languages section"""
        return self.config.get('packaging_languages', {})
    
    def get_server_region(self) -> Dict[str, Any]:
        """Get server region section"""
        return self.config.get('server_region', {})
    
    def get_host_info(self) -> Dict[str, Any]:
        """Get host information section"""
        return self.config.get('host', {})
    
    def get_social_links(self) -> Dict[str, Any]:
        """Get social links section"""
        return self.config.get('social', {})
    
    def auto_detect_and_update_environment(self) -> None:
        """Auto-detect environment information and update configuration"""
        # Skip auto-detection if running in GitHub Actions to preserve local environment info
        # This ensures the SVG shows your local environment (macOS) instead of the GitHub Actions runner (Ubuntu)
        if os.getenv('GITHUB_ACTIONS') == 'true':
            print("🔄 Running in GitHub Actions - preserving local environment configuration")
            return
        
        try:
            detected_env = auto_detect_environment()
            
            # Update environment section
            if 'environment' not in self.config:
                self.config['environment'] = {}
            
            self.config['environment'].update(detected_env)
            print(f"✅ Auto-detected environment: {detected_env['os']} {detected_env['version']} • {detected_env['editor']}")
            
        except Exception as e:
            print(f"⚠️  Auto-detection failed: {e}")
    
    def validate_config(self) -> bool:
        """Validate that required configuration sections exist"""
        required_sections = ['environment', 'packaging_languages', 'server_region', 'host', 'social']
        
        for section in required_sections:
            if section not in self.config:
                print(f"❌ Missing required configuration section: {section}")
                return False
        
        # Validate environment section
        environment = self.config['environment']
        if 'os' not in environment:
            print("❌ Missing required field: environment.os")
            return False
        
        # Validate packaging_languages section
        packaging_languages = self.config['packaging_languages']
        if 'languages' not in packaging_languages:
            print("❌ Missing required field: packaging_languages.languages")
            return False
        
        # Validate server_region section
        server_region = self.config['server_region']
        if 'region' not in server_region:
            print("❌ Missing required field: server_region.region")
            return False
        
        # Validate host section
        host = self.config['host']
        if 'platform' not in host:
            print("❌ Missing required field: host.platform")
            return False
        
        return True


# Global configuration instance
config = ConfigManager() 
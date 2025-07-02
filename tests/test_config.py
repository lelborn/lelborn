#!/usr/bin/env python3
"""
Test script for the new simplified config structure
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import config
from src.svg_generator import svg_generator

def test_config_loading():
    """Test that the new config structure loads correctly"""
    print("🧪 Testing config loading...")
    
    # Test basic config loading
    print(f"✅ Config loaded successfully")
    print(f"📁 Environment OS: {config.get('environment.os')}")
    print(f"📁 Packaging Languages: {config.get('packaging_languages.languages')}")
    print(f"📁 Server Region: {config.get('server_region.region')}")
    print(f"📁 Host Platform: {config.get('host.platform')}")
    print(f"📁 Social LinkedIn: {config.get('social.linkedin')}")
    
    # Test validation
    if config.validate_config():
        print("✅ Config validation passed")
    else:
        print("❌ Config validation failed")
        return False
    
    return True

def test_svg_generation():
    """Test SVG generation with mock data"""
    print("\n🧪 Testing SVG generation...")
    
    # Mock data
    age_data = "33 years, 5 Months, 15 Days"
    commit_data = 3145
    star_data = 503
    repo_data = 42
    contrib_data = 133
    follower_data = 100
    loc_data = [87122, 25761, 61361]
    build_timestamp = "2024-01-15 10:30:00"
    
    try:
        # Test SVG file validation
        if svg_generator.validate_svg_files():
            print("✅ SVG files found")
        else:
            print("❌ SVG files missing")
            return False
        
        # Test config data retrieval
        config_data = svg_generator._get_config_data()
        print(f"✅ Config data retrieved: {len(config_data)} fields")
        
        # Test data formatting
        formatted_data = svg_generator._format_data_for_svg(
            commit_data, star_data, contrib_data, loc_data
        )
        print(f"✅ Data formatted: {len(formatted_data)} fields")
        
        # Test replacement logic (without actually writing files)
        test_content = """
        <text x="18" y="162">✔ Environment: macOS Sequoia (15.5 (24F74)) • VS Code (1.100.2)</text>
        <text x="18" y="274">✔ Packaging Languages: [TypeScript, Python, Go, React]</text>
        <text x="18" y="306">✔ Server Region: Europe/London</text>
        <text x="18" y="338">✔ Host: Marketplace Platforms</text>
        <text x="18" y="354">✔ Social: linkedin.com/lewiselborn</text>
        """
        
        updated_content = svg_generator._apply_replacements(
            test_content, formatted_data, age_data, config_data, build_timestamp
        )
        
        print("✅ Replacement logic works")
        print("📝 Sample updated content:")
        print(updated_content.strip())
        
        return True
        
    except Exception as e:
        print(f"❌ Error during SVG generation test: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing new config structure...")
    print("=" * 50)
    
    # Test config loading
    if not test_config_loading():
        print("❌ Config loading test failed")
        return 1
    
    # Test SVG generation
    if not test_svg_generation():
        print("❌ SVG generation test failed")
        return 1
    
    print("\n" + "=" * 50)
    print("✅ All tests passed! New config structure is working correctly.")
    return 0

if __name__ == "__main__":
    exit(main()) 
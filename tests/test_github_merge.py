#!/usr/bin/env python3
"""
Test script to verify GitHub data merging functionality
"""

def test_github_data_merging():
    """Test that GitHub data is properly merged with configuration"""
    
    from src.config import ConfigManager
    
    # Create a test config manager
    test_config = ConfigManager()
    
    # Mock GitHub data
    mock_github_data = {
        'created_at': '2020-01-15T10:30:00Z',
        'location': 'San Francisco, CA',
        'website': 'https://example.com',
        'email': 'test@example.com',
        'twitter': 'testuser',
        'bio': 'Software Developer',
        'company': 'Tech Corp',
        'is_hireable': True
    }
    
    print("🧪 Testing GitHub Data Merging")
    print("=" * 40)
    
    # Test before merging
    print("Before merging:")
    print(f"  Location: {test_config.get('personal.location', 'Not set')}")
    print(f"  Website: {test_config.get('social.website', 'Not set')}")
    print(f"  Email: {test_config.get('social.email', 'Not set')}")
    print(f"  Twitter: {test_config.get('social.twitter', 'Not set')}")
    
    # Merge GitHub data
    test_config.merge_github_data(mock_github_data)
    
    print("\nAfter merging:")
    print(f"  Location: {test_config.get('personal.location', 'Not set')}")
    print(f"  Website: {test_config.get('social.website', 'Not set')}")
    print(f"  Email: {test_config.get('social.email', 'Not set')}")
    print(f"  Twitter: {test_config.get('social.twitter', 'Not set')}")
    print(f"  GitHub joined: {test_config.get('personal.github_joined', 'Not set')}")
    
    # Verify the merging worked
    expected_values = {
        'personal.location': 'San Francisco, CA',
        'social.website': 'https://example.com',
        'social.email': 'test@example.com',
        'social.twitter': 'twitter.com/testuser',
        'personal.github_joined': '2020-01-15T10:30:00Z'
    }
    
    all_correct = True
    for key, expected in expected_values.items():
        actual = test_config.get(key, 'Not set')
        if actual == expected:
            print(f"✅ {key}: {actual}")
        else:
            print(f"❌ {key}: expected '{expected}', got '{actual}'")
            all_correct = False
    
    return all_correct


def test_config_override():
    """Test that profile_config.json values can override GitHub data"""
    
    from src.config import ConfigManager
    
    # Create a test config manager
    test_config = ConfigManager()
    
    # Set a value in config that should override GitHub data
    test_config.config['personal']['location'] = 'Custom Location'
    
    # Mock GitHub data with different location
    mock_github_data = {
        'location': 'GitHub Location',
        'website': 'https://github.com',
        'email': 'github@example.com'
    }
    
    print("\n🧪 Testing Config Override")
    print("=" * 40)
    
    print("Before merging:")
    print(f"  Location: {test_config.get('personal.location')}")
    
    # Merge GitHub data
    test_config.merge_github_data(mock_github_data)
    
    print("After merging:")
    print(f"  Location: {test_config.get('personal.location')}")
    print(f"  Website: {test_config.get('social.website')}")
    
    # GitHub data should override config for fields that weren't set
    # but config should override for fields that were already set
    if test_config.get('personal.location') == 'Custom Location':
        print("✅ Config override works correctly")
        return True
    else:
        print("❌ Config override failed")
        return False


def main():
    """Run all GitHub data merging tests"""
    print("🚀 Testing GitHub Data Integration")
    print("=" * 50)
    
    tests = [
        test_github_data_merging,
        test_config_override
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("✅ All GitHub data merging tests passed!")
    else:
        print("❌ Some tests failed.")


if __name__ == "__main__":
    main() 
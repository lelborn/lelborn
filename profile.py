#!/usr/bin/env python3
"""
GitHub Profile Generator - Main Script
Generates dynamic GitHub profile README with real-time statistics

Author: Lewis Elborn (lelborn)
Adapted from: Andrew Grant (Andrew6rant), 2022-2025
Version: 2.0.0
"""

import datetime
import sys
from typing import List, Tuple
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import our modular components
from src import (
    config,
    svg_generator,
    calculate_age,
    measure_performance,
    format_performance_output,
    ensure_directory_exists
)
from src.utils import generate_build_timestamp
from src.github_api import get_github_api


class ProfileGenerator:
    """Main profile generator class"""
    
    def __init__(self):
        """Initialize the profile generator"""
        self.performance_times = {}
        
        # Ensure required directories exist
        ensure_directory_exists('cache')
        
        # Validate configuration
        if not config.validate_config():
            print("❌ Configuration validation failed")
            sys.exit(1)
        
        # Auto-detect environment information
        config.auto_detect_and_update_environment()
        
        # Validate SVG files
        if not svg_generator.validate_svg_files():
            print("❌ SVG file validation failed")
            sys.exit(1)
    
    def run(self) -> None:
        """Main execution method"""
        print("🚀 Starting GitHub Profile Generator...")
        print("=" * 50)
        
        try:
            # Collect all data
            data = self._collect_data()
            
            # Update SVG files
            self._update_svg_files(data)
            
            # Display performance summary
            self._display_performance_summary()
            
            print("=" * 50)
            print("✅ Profile generation completed successfully!")
            
        except Exception as e:
            print(f"❌ Error during profile generation: {e}")
            sys.exit(1)
    
    def _collect_data(self) -> dict:
        """Collect all required data from GitHub API"""
        print("📊 Collecting GitHub data...")
        
        data = {}
        
        # Get user information
        github_api = get_github_api()
        user_data, user_time = measure_performance(github_api.get_user_info)
        self.performance_times['user_info'] = user_time
        format_performance_output('user info', user_time)
        data['user_id'], data['github_info'] = user_data
        
        # Merge GitHub data with configuration
        config.merge_github_data(data['github_info'])
        
        # Calculate age
        birthday_str = config.get('personal.birthday')
        birthday = datetime.datetime.strptime(birthday_str, "%Y-%m-%d")
        age_data, age_time = measure_performance(calculate_age, birthday)
        self.performance_times['age_calculation'] = age_time
        format_performance_output('age calculation', age_time)
        data['age'] = age_data
        
        # Get repository statistics
        data['stars'], star_time = self._get_repository_stats('stars', ['OWNER'])
        self.performance_times['stars'] = star_time
        print(f"DEBUG: Stars: {data['stars']}")
        
        data['repos'], repo_time = self._get_repository_stats('repos', ['OWNER'])
        self.performance_times['repos'] = repo_time
        print(f"DEBUG: Repos: {data['repos']}")
        
        data['contrib_repos'], contrib_time = self._get_repository_stats('repos', 
                                                                       ['OWNER', 'COLLABORATOR', 'ORGANIZATION_MEMBER'])
        self.performance_times['contrib_repos'] = contrib_time
        print(f"DEBUG: Contributed Repos: {data['contrib_repos']}")
        
        # Get follower count
        data['followers'], follower_time = measure_performance(github_api.get_follower_count)
        self.performance_times['followers'] = follower_time
        format_performance_output('followers', follower_time)
        print(f"DEBUG: Followers: {data['followers']}")
        
        # Get lines of code from GitHub API
        data['loc_data'], loc_time = measure_performance(self._get_lines_of_code)
        self.performance_times['lines_of_code'] = loc_time
        format_performance_output('lines of code', loc_time)
        print(f"DEBUG: LOC Data: {data['loc_data']}")
        
        # Get commit count from GitHub API
        data['commits'], commit_time = measure_performance(self._get_commit_count)
        self.performance_times['commits'] = commit_time
        format_performance_output('commits', commit_time)
        print(f"DEBUG: Commits: {data['commits']}")
        
        return data
    
    def _get_repository_stats(self, stat_type: str, affiliations: List[str]) -> Tuple[int, float]:
        """Get repository statistics with performance measurement"""
        github_api = get_github_api()
        result, time_taken = measure_performance(
            github_api.get_repository_stats, stat_type, affiliations
        )
        format_performance_output(f'{stat_type} count', time_taken)
        return result, time_taken
    
    def _get_lines_of_code(self) -> List[int]:
        """Get lines of code statistics from GitHub API"""
        github_api = get_github_api()
        # Get LOC data for owned repositories
        loc_data = github_api.get_lines_of_code(['OWNER'])
        # Return [added, deleted, total] format expected by SVG generator
        return [loc_data[0], loc_data[1], loc_data[2]]
    
    def _get_commit_count(self) -> int:
        """Get total commit count from GitHub API"""
        github_api = get_github_api()
        # Get commit count for the last year
        from datetime import datetime, timedelta
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        return github_api.get_commit_stats(
            start_date.isoformat(),
            end_date.isoformat()
        )
    
    def _update_svg_files(self, data: dict) -> None:
        """Update SVG files with collected data"""
        print("\n🎨 Updating SVG files...")
        
        # Generate build timestamp
        build_timestamp = generate_build_timestamp()
        
        svg_generator.update_svg_files(
            age_data=data['age'],
            commit_data=data['commits'],
            star_data=data['stars'],
            repo_data=data['repos'],
            contrib_data=data['contrib_repos'],
            follower_data=data['followers'],
            loc_data=data['loc_data'],
            build_timestamp=build_timestamp
        )
    
    def _display_performance_summary(self) -> None:
        """Display performance summary and API usage statistics"""
        print("\n📈 Performance Summary:")
        print("-" * 30)
        
        # Calculate total time
        total_time = sum(self.performance_times.values())
        format_performance_output('total time', total_time)
        
        # Display API usage
        github_api = get_github_api()
        query_stats = github_api.get_query_stats()
        total_queries = github_api.get_total_queries()
        
        print(f"\n🔌 API Usage:")
        print(f"   Total queries: {total_queries}")
        for operation, count in query_stats.items():
            if count > 0:
                print(f"   {operation}: {count}")


def main():
    """Main entry point"""
    try:
        generator = ProfileGenerator()
        generator.run()
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 
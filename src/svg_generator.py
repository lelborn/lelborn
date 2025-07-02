"""
SVG Generator for GitHub Profile
Handles updating SVG files with GitHub statistics and configuration data
"""

from typing import List, Dict, Any
from .config import config
from .utils import format_number


class SVGGenerator:
    """Handles SVG file generation and updates"""
    
    def __init__(self):
        """Initialize SVG generator"""
        self.dark_mode_file = 'profile-dark.svg'
        self.light_mode_file = 'profile-light.svg'
    
    def update_svg_files(self, age_data: str, commit_data: int, star_data: int, 
                        repo_data: int, contrib_data: int, follower_data: int, 
                        loc_data: List[int], build_timestamp: str = None) -> None:
        """
        Update both dark and light mode SVG files with current data
        
        Args:
            age_data: Formatted age string
            commit_data: Total commit count
            star_data: Total star count
            repo_data: Repository count
            contrib_data: Contributed repository count
            follower_data: Follower count
            loc_data: [added_loc, deleted_loc, total_loc]
        """
        print("🔄 Updating SVG files...")
        
        # Update dark mode SVG
        self._update_single_svg(self.dark_mode_file, age_data, commit_data, 
                               star_data, repo_data, contrib_data, follower_data, loc_data, build_timestamp)
        
        # Update light mode SVG
        self._update_single_svg(self.light_mode_file, age_data, commit_data, 
                               star_data, repo_data, contrib_data, follower_data, loc_data, build_timestamp)
        
        print("✅ SVG files updated successfully")
    
    def _update_single_svg(self, filename: str, age_data: str, commit_data: int, 
                          star_data: int, repo_data: int, contrib_data: int, 
                          follower_data: int, loc_data: List[int], build_timestamp: str = None) -> None:
        """
        Update a single SVG file with current data
        """
        try:
            # Read the SVG file
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Format the data for display
            formatted_data = self._format_data_for_svg(
                commit_data, star_data, contrib_data, loc_data
            )
            
            # Get configuration data
            config_data = self._get_config_data()
            
            # Apply all replacements
            content = self._apply_replacements(content, formatted_data, age_data, config_data, build_timestamp)
            
            # Write the updated content back to the file
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
                
        except FileNotFoundError:
            print(f"⚠️  Warning: {filename} not found, skipping update")
        except Exception as e:
            print(f"❌ Error updating {filename}: {e}")
    
    def _format_data_for_svg(self, commit_data: int, star_data: int, 
                            contrib_data: int, loc_data: List[int]) -> Dict[str, str]:
        """
        Format data for SVG replacement
        """
        return {
            'commit_formatted': format_number(commit_data),
            'star_formatted': format_number(star_data),
            'contrib_formatted': format_number(contrib_data),
            'loc_add_formatted': format_number(loc_data[0]),
            'loc_del_formatted': format_number(loc_data[1]),
            'loc_total_formatted': format_number(loc_data[2])
        }
    
    def _get_config_data(self) -> Dict[str, str]:
        """
        Get configuration data for SVG replacement
        """
        return {
            'server_region': config.get('server_region.region', 'Europe/London'),
            'host_platform': config.get('host.platform', 'Marketplace Platforms'),
            'environment_os': config.get('environment.os', 'macOS Sequoia'),
            'environment_version': config.get('environment.version', '15.5 (24F74)'),
            'environment_editor': config.get('environment.editor', 'VS Code (1.100.2)'),
            'packaging_languages': ', '.join(config.get('packaging_languages.languages', ['TypeScript', 'Python', 'Go', 'React'])),
            'social_linkedin': config.get('social.linkedin', 'linkedin.com/lewiselborn'),
            'social_twitter': config.get('social.twitter', 'twitter.com/lelborn'),
            'social_website': config.get('social.website', 'lewiselborn.com'),
            'social_email': config.get('social.email', 'lewis@lewiselborn.com')
        }
    
    def _apply_replacements(self, content: str, formatted_data: Dict[str, str], 
                           age_data: str, config_data: Dict[str, str], build_timestamp: str = None) -> str:
        """
        Apply all text replacements to SVG content
        """
        # GitHub statistics replacements
        content = content.replace("{COMMITS}", formatted_data['commit_formatted'])
        content = content.replace("{CONTRIB}", formatted_data['contrib_formatted'])
        content = content.replace("{STARS}", formatted_data['star_formatted'])
        
        # LOC replacements
        content = content.replace("{LOC_TOTAL}", formatted_data['loc_total_formatted'])
        content = content.replace("{LOC_ADD}", formatted_data['loc_add_formatted'])
        content = content.replace("{LOC_DEL}", formatted_data['loc_del_formatted'])
        
        # Age replacement
        content = content.replace("{AGE}", age_data)
        
        # Environment replacements
        content = content.replace("{ENVIRONMENT}", 
                                f"{config_data['environment_os']} ({config_data['environment_version']}) • {config_data['environment_editor']}")
        
        # Packaging languages replacement
        content = content.replace("{LANGUAGES}", config_data['packaging_languages'])
        
        # Server region replacement
        content = content.replace("{SERVER_REGION}", config_data['server_region'])
        
        # Host replacement
        content = content.replace("{HOST_PLATFORM}", config_data['host_platform'])
        
        # Social replacements
        content = content.replace("{LINKEDIN}", config_data['social_linkedin'])
        content = content.replace("twitter.com/lelborn", config_data['social_twitter'])
        content = content.replace("lewiselborn.com", config_data['social_website'])
        content = content.replace("lewis@lewiselborn.com", config_data['social_email'])
        
        # Build timestamp replacement
        if build_timestamp:
            content = content.replace("{BUILD_TIMESTAMP}", build_timestamp)
        
        return content
    
    def validate_svg_files(self) -> bool:
        """
        Validate that required SVG files exist
        """
        missing_files = []
        
        if not self._file_exists(self.dark_mode_file):
            missing_files.append(self.dark_mode_file)
        
        if not self._file_exists(self.light_mode_file):
            missing_files.append(self.light_mode_file)
        
        if missing_files:
            print(f"❌ Missing required SVG files: {', '.join(missing_files)}")
            return False
        
        return True
    
    def _file_exists(self, filename: str) -> bool:
        """Check if a file exists"""
        import os
        return os.path.exists(filename)


# Global SVG generator instance
svg_generator = SVGGenerator() 
"""
GitHub Profile Generator Package
A modular system for generating dynamic GitHub profile READMEs
"""

from .config import config, ConfigManager
from .github_api import get_github_api, GitHubAPI
from .svg_generator import svg_generator, SVGGenerator
from .utils import (
    calculate_age,
    format_number,
    measure_performance,
    format_performance_output,
    ensure_directory_exists,
    generate_build_timestamp
)

__version__ = "2.0.0"
__author__ = "Lewis Elborn"
__email__ = "lewis@lewiselborn.com"

__all__ = [
    'config',
    'ConfigManager',
    'get_github_api',
    'GitHubAPI',
    'svg_generator',
    'SVGGenerator',
    'calculate_age',
    'format_number',
    'measure_performance',
    'format_performance_output',
    'ensure_directory_exists',
    'generate_build_timestamp'
] 
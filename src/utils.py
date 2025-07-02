"""
Utility functions for GitHub Profile Generator
Common helper functions used across the application
"""

import time
import datetime
import platform
import os
import subprocess
from dateutil import relativedelta
from typing import Any, Tuple


def format_plural(unit: int) -> str:
    """
    Returns a properly formatted plural suffix
    e.g., format_plural(5) -> 's', format_plural(1) -> ''
    """
    return 's' if unit != 1 else ''


def calculate_age(birthday: datetime.datetime) -> str:
    """
    Calculate age from birthday and return formatted string
    e.g., '33 years, 5 months, 15 days'
    """
    diff = relativedelta.relativedelta(datetime.datetime.today(), birthday)
    
    age_parts = []
    if diff.years > 0:
        age_parts.append(f"{diff.years} year{format_plural(diff.years)}")
    if diff.months > 0:
        age_parts.append(f"{diff.months} month{format_plural(diff.months)}")
    if diff.days > 0:
        age_parts.append(f"{diff.days} day{format_plural(diff.days)}")
    
    # Handle edge case where all are 0
    if not age_parts:
        age_parts.append("0 days")
    
    age_str = ", ".join(age_parts)
    
    # Add birthday emoji if it's today
    if diff.months == 0 and diff.days == 0:
        age_str += " 🎂"
    
    return age_str


def format_number(number: int) -> str:
    """
    Format number with thousands separators
    e.g., 1234567 -> '1,234,567'
    """
    return f"{number:,}"


def measure_performance(func: callable, *args) -> Tuple[Any, float]:
    """
    Measure the execution time of a function
    Returns (function_result, execution_time_in_seconds)
    """
    start_time = time.perf_counter()
    result = func(*args)
    end_time = time.perf_counter()
    
    return result, end_time - start_time


def format_performance_output(operation_name: str, execution_time: float, result: Any = None, 
                            whitespace: int = 0) -> str:
    """
    Format performance output for display
    """
    # Format the operation name with padding
    formatted_name = f"   {operation_name}:".ljust(23)
    
    # Format the execution time
    if execution_time > 1:
        time_str = f"{execution_time:.4f} s "
    else:
        time_str = f"{execution_time * 1000:.4f} ms"
    
    formatted_time = time_str.rjust(12)
    
    # Print the performance line
    print(f"{formatted_name}{formatted_time}")
    
    # Return formatted result if requested
    if result is not None and whitespace > 0:
        return f"{format_number(result): <{whitespace}}"
    
    return result


def ensure_directory_exists(directory_path: str) -> None:
    """
    Ensure a directory exists, create it if it doesn't
    """
    os.makedirs(directory_path, exist_ok=True)


def safe_file_read(file_path: str, default_content: str = "") -> str:
    """
    Safely read a file, return default content if file doesn't exist
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return default_content


def safe_file_write(file_path: str, content: str) -> None:
    """
    Safely write content to a file
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


def generate_build_timestamp() -> str:
    """
    Generate a build timestamp in BST (British Summer Time) in the format used by terminal 'last login'
    e.g., 'Tue Jun 3 14:01:52'
    """
    # Get current time in UTC
    utc_time = datetime.datetime.utcnow()
    
    # Convert to BST (UTC+1 during summer time)
    # Note: This is a simplified approach - for production use, consider using pytz or zoneinfo
    bst_time = utc_time + datetime.timedelta(hours=1)
    
    return bst_time.strftime("%a %b %-d %H:%M:%S")


def detect_os_info() -> Tuple[str, str]:
    """
    Detect operating system and version with build details
    Returns (os_name, version)
    """
    system = platform.system()
    
    if system == "Darwin":  # macOS
        try:
            # Get macOS version
            result = subprocess.run(['sw_vers', '-productVersion'], 
                                  capture_output=True, text=True, check=True)
            version = result.stdout.strip()
            
            # Get macOS name
            result = subprocess.run(['sw_vers', '-productName'], 
                                  capture_output=True, text=True, check=True)
            os_name = result.stdout.strip()
            
            # Get build version
            result = subprocess.run(['sw_vers', '-buildVersion'], 
                                  capture_output=True, text=True, check=True)
            build_version = result.stdout.strip()
            
            # Get kernel version
            kernel_version = platform.release()
            
            # Format: macOS 15.5 (24F74) • Darwin 23.5.0
            formatted_version = f"{version} ({build_version}) • Darwin {kernel_version}"
            
            return os_name, formatted_version
        except subprocess.CalledProcessError:
            return "macOS", "Unknown"
    
    elif system == "Windows":
        try:
            # Get Windows version
            result = subprocess.run(['ver'], capture_output=True, text=True, check=True)
            version = result.stdout.strip()
            
            # Get Windows build number
            result = subprocess.run(['wmic', 'os', 'get', 'BuildNumber', '/value'], 
                                  capture_output=True, text=True, check=True)
            build_line = result.stdout.strip()
            build_number = build_line.split('=')[1] if '=' in build_line else "Unknown"
            
            # Get kernel version
            kernel_version = platform.release()
            
            # Format: Windows 10.0.19045 (19045) • NT 10.0
            formatted_version = f"{version} ({build_number}) • NT {kernel_version}"
            
            return "Windows", formatted_version
        except subprocess.CalledProcessError:
            return "Windows", "Unknown"
    
    elif system == "Linux":
        try:
            # Try to get Linux distribution info
            if os.path.exists('/etc/os-release'):
                with open('/etc/os-release', 'r') as f:
                    lines = f.readlines()
                    name = "Linux"
                    version = "Unknown"
                    
                    for line in lines:
                        if line.startswith('PRETTY_NAME='):
                            name = line.split('=')[1].strip().strip('"')
                        elif line.startswith('VERSION='):
                            version = line.split('=')[1].strip().strip('"')
                    
                    # Get kernel version
                    kernel_version = platform.release()
                    
                    # Format: Ubuntu 22.04.3 LTS • Linux 5.15.0
                    formatted_version = f"{version} • Linux {kernel_version}"
                    
                    return name, formatted_version
            else:
                kernel_version = platform.release()
                return "Linux", f"Unknown • Linux {kernel_version}"
        except Exception:
            return "Linux", "Unknown"
    
    else:
        return system, "Unknown"


def detect_editor() -> str:
    """
    Detect the current editor from environment variables
    """
    # Check common editor environment variables
    editor_vars = ['EDITOR', 'VISUAL', 'VSCODE_PID', 'TERM_PROGRAM']
    
    for var in editor_vars:
        if var in os.environ:
            editor = os.environ[var]
            
            if 'code' in editor.lower() or 'vscode' in editor.lower():
                return "VS Code"
            elif 'vim' in editor.lower():
                return "Vim"
            elif 'emacs' in editor.lower():
                return "Emacs"
            elif 'nano' in editor.lower():
                return "Nano"
            elif 'sublime' in editor.lower():
                return "Sublime Text"
    
    # Check if VS Code is running
    try:
        result = subprocess.run(['pgrep', '-f', 'code'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            return "VS Code"
    except:
        pass
    
    return "Unknown Editor"


def get_editor_version(editor: str) -> str:
    """
    Get version information for the detected editor with build details
    """
    try:
        if editor == "VS Code":
            # Try to get VS Code version
            result = subprocess.run(['code', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                version = lines[0]  # Main version
                commit_hash = lines[1] if len(lines) > 1 else ""  # Commit hash
                architecture = platform.machine()  # Architecture
                
                # Format: (1.1.6) • x64 • a1b2c3d
                formatted_version = f"({version}) • {architecture}"
                if commit_hash:
                    formatted_version += f" • {commit_hash[:8]}"
                
                return formatted_version
        elif editor == "Vim":
            result = subprocess.run(['vim', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                # Extract version from first line
                version_line = result.stdout.split('\n')[0]
                if 'VIM' in version_line:
                    version = version_line.split()[4]
                    architecture = platform.machine()
                    return f"({version}) • {architecture}"
        elif editor == "Emacs":
            result = subprocess.run(['emacs', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                if 'GNU Emacs' in version_line:
                    version = version_line.split()[2]
                    architecture = platform.machine()
                    return f"({version}) • {architecture}"
    except:
        pass
    
    return ""


def get_system_info() -> dict:
    """
    Get additional system information for techy display
    """
    info = {}
    
    # Python version
    info['python_version'] = f"Python {platform.python_version()}"
    
    # Architecture
    info['architecture'] = platform.machine()
    
    # Processor
    info['processor'] = platform.processor()
    
    # Platform
    info['platform'] = platform.platform()
    
    return info


def auto_detect_environment() -> dict:
    """
    Automatically detect environment information
    Returns dict with os, version, and editor
    """
    os_name, os_version = detect_os_info()
    editor = detect_editor()
    editor_version = get_editor_version(editor)
    
    return {
        'os': os_name,
        'version': os_version,
        'editor': f"{editor} {editor_version}".strip()
    } 
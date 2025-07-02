"""
System detection utilities for GitHub Profile Generator
Handles OS detection, editor detection, and system information gathering
"""

import platform
import os
import subprocess
from typing import Tuple, Dict


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
    
    return "Unknown"


def get_system_info() -> Dict[str, str]:
    """
    Get comprehensive system information
    Returns a dictionary with OS, editor, and other system details
    """
    os_name, os_version = detect_os_info()
    editor = detect_editor()
    editor_version = get_editor_version(editor)
    
    return {
        'os': os_name,
        'version': os_version,
        'editor': f"{editor} {editor_version}"
    }


def auto_detect_environment() -> Dict[str, str]:
    """
    Auto-detect and return environment information
    This is a convenience function that returns the same data as get_system_info()
    """
    return get_system_info() 
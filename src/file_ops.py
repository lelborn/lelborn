"""
File operations utilities for GitHub Profile Generator
Handles file reading, writing, and directory operations
"""

import os


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
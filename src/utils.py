"""
Utility functions for GitHub Profile Generator
Common helper functions used across the application
"""

import time
import datetime
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
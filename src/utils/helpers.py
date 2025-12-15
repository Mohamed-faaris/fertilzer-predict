"""
Utility helper functions
"""
import pandas as pd
import numpy as np
from datetime import datetime
import sys
sys.path.append('/home/faaris/projects/BDA/fert-predict')
from config.settings import COLOR_PALETTE, FERTILIZER_COLORS, SOIL_COLORS, CROP_COLORS


def format_number(num: float, decimals: int = 2) -> str:
    """Format number with commas and decimals"""
    if pd.isna(num):
        return "N/A"
    return f"{num:,.{decimals}f}"


def format_percentage(num: float, decimals: int = 1) -> str:
    """Format number as percentage"""
    if pd.isna(num):
        return "N/A"
    return f"{num:.{decimals}f}%"


def get_color_for_fertilizer(fertilizer: str) -> str:
    """Get color for fertilizer type"""
    return FERTILIZER_COLORS.get(fertilizer, COLOR_PALETTE['primary'])


def get_color_for_soil(soil: str) -> str:
    """Get color for soil type"""
    return SOIL_COLORS.get(soil, COLOR_PALETTE['secondary'])


def get_color_for_crop(crop: str) -> str:
    """Get color for crop type"""
    return CROP_COLORS.get(crop, COLOR_PALETTE['accent'])


def get_fertilizer_colors_list() -> list:
    """Get list of fertilizer colors"""
    return list(FERTILIZER_COLORS.values())


def get_soil_colors_list() -> list:
    """Get list of soil colors"""
    return list(SOIL_COLORS.values())


def get_crop_colors_list() -> list:
    """Get list of crop colors"""
    return list(CROP_COLORS.values())


def calculate_delta(current: float, previous: float) -> tuple:
    """
    Calculate delta and percentage change
    
    Returns:
        Tuple of (delta, percentage_change)
    """
    if previous == 0:
        return (current, 100.0 if current > 0 else 0.0)
    
    delta = current - previous
    pct_change = (delta / previous) * 100
    return (delta, pct_change)


def export_to_csv(df: pd.DataFrame, filename: str):
    """Export DataFrame to CSV"""
    df.to_csv(filename, index=False)
    return filename


def export_to_excel(df: pd.DataFrame, filename: str):
    """Export DataFrame to Excel"""
    df.to_excel(filename, index=False, engine='openpyxl')
    return filename


def get_timestamp() -> str:
    """Get current timestamp string"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def create_download_filename(prefix: str, extension: str = "csv") -> str:
    """Create filename for downloads"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{extension}"


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers"""
    if denominator == 0:
        return default
    return numerator / denominator


def get_status_color(value: float, thresholds: dict) -> str:
    """
    Get status color based on thresholds
    
    Args:
        value: Value to check
        thresholds: Dict with 'good', 'warning', 'danger' keys
        
    Returns:
        Color code
    """
    if value >= thresholds.get('good', 80):
        return COLOR_PALETTE['success']
    elif value >= thresholds.get('warning', 50):
        return COLOR_PALETTE['warning']
    else:
        return COLOR_PALETTE['danger']

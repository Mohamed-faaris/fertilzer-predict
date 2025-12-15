"""
Configuration settings for the Fertilizer Prediction Application
"""
import os
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
CACHE_DIR = BASE_DIR / ".cache"

# Data files
MAIN_DATA_FILE = DATA_DIR / "Fertilizer Prediction.csv"
SMALL_DATA_FILE = DATA_DIR / "small.csv"

# Spark configuration
SPARK_CONFIG = {
    "spark.app.name": "FertilizerPrediction",
    "spark.master": "local[*]",
    "spark.driver.memory": "4g",
    "spark.executor.memory": "4g",
    "spark.sql.shuffle.partitions": "8",
    "spark.default.parallelism": "8",
}

# UI Configuration
APP_TITLE = "🌾 Fertilizer Prediction & Analytics"
APP_ICON = "🌾"
PAGE_CONFIG = {
    "page_title": "Fertilizer Analytics",
    "page_icon": "🌾",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# Color schemes for visualizations
COLOR_PALETTE = {
    "primary": "#4CAF50",
    "secondary": "#2196F3",
    "accent": "#FF9800",
    "success": "#8BC34A",
    "warning": "#FFC107",
    "danger": "#F44336",
    "info": "#00BCD4",
}

FERTILIZER_COLORS = {
    "Urea": "#FF6B6B",
    "DAP": "#4ECDC4",
    "14-35-14": "#45B7D1",
    "28-28": "#96CEB4",
    "20-20": "#FFEAA7",
    "17-17-17": "#DFE6E9",
    "10-26-26": "#A29BFE",
}

SOIL_COLORS = {
    "Red": "#E74C3C",
    "Black": "#34495E",
    "Sandy": "#F39C12",
    "Loamy": "#8B4513",
    "Clayey": "#95A5A6",
}

CROP_COLORS = {
    "Wheat": "#F4D03F",
    "Cotton": "#FFFFFF",
    "Paddy": "#52BE80",
    "Maize": "#F8C471",
    "Sugarcane": "#A9DFBF",
    "Barley": "#D4AC0D",
    "Tobacco": "#7D6608",
    "Millets": "#E59866",
    "Oil seeds": "#F7DC6F",
    "Pulses": "#76D7C4",
    "Ground Nuts": "#C39BD3",
}

# Feature names
FEATURE_COLUMNS = [
    "Temparature",
    "Humidity", 
    "Moisture",
    "Soil Type",
    "Crop Type",
    "Nitrogen",
    "Potassium",
    "Phosphorous",
]

TARGET_COLUMN = "Fertilizer Name"

# Categorical features
CATEGORICAL_FEATURES = ["Soil Type", "Crop Type"]
NUMERICAL_FEATURES = ["Temparature", "Humidity", "Moisture", "Nitrogen", "Potassium", "Phosphorous"]

# Valid values
SOIL_TYPES = ["Red", "Black", "Sandy", "Loamy", "Clayey"]
CROP_TYPES = [
    "Wheat", "Cotton", "Paddy", "Maize", "Sugarcane",
    "Barley", "Tobacco", "Millets", "Oil seeds", "Pulses", "Ground Nuts"
]
FERTILIZER_TYPES = ["Urea", "DAP", "14-35-14", "28-28", "20-20", "17-17-17", "10-26-26"]

# Create cache directory if it doesn't exist
CACHE_DIR.mkdir(exist_ok=True)

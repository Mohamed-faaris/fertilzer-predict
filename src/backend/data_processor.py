"""
Data preprocessing and feature engineering module
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
import sys
sys.path.append('/home/faaris/projects/BDA/fert-predict')
from config.settings import (
    CATEGORICAL_FEATURES, NUMERICAL_FEATURES,
    SOIL_TYPES, CROP_TYPES, FERTILIZER_TYPES
)
import logging

logger = logging.getLogger(__name__)


class DataProcessor:
    """Data preprocessing and validation"""
    
    def __init__(self):
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.is_fitted = False
    
    def validate_data(self, df: pd.DataFrame) -> dict:
        """
        Validate data quality
        
        Args:
            df: Pandas DataFrame
            
        Returns:
            Dictionary with validation results
        """
        results = {
            'total_records': len(df),
            'missing_values': {},
            'invalid_values': {},
            'duplicates': df.duplicated().sum(),
            'data_types': {},
        }
        
        # Check missing values
        for col in df.columns:
            missing = df[col].isna().sum()
            if missing > 0:
                results['missing_values'][col] = missing
        
        # Check invalid categorical values
        if 'Soil Type' in df.columns:
            invalid_soil = df[~df['Soil Type'].isin(SOIL_TYPES)]['Soil Type'].unique()
            if len(invalid_soil) > 0:
                results['invalid_values']['Soil Type'] = invalid_soil.tolist()
        
        if 'Crop Type' in df.columns:
            invalid_crop = df[~df['Crop Type'].isin(CROP_TYPES)]['Crop Type'].unique()
            if len(invalid_crop) > 0:
                results['invalid_values']['Crop Type'] = invalid_crop.tolist()
        
        if 'Fertilizer Name' in df.columns:
            invalid_fert = df[~df['Fertilizer Name'].isin(FERTILIZER_TYPES)]['Fertilizer Name'].unique()
            if len(invalid_fert) > 0:
                results['invalid_values']['Fertilizer Name'] = invalid_fert.tolist()
        
        # Check data types
        for col in df.columns:
            results['data_types'][col] = str(df[col].dtype)
        
        return results
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and prepare data
        
        Args:
            df: Pandas DataFrame
            
        Returns:
            Cleaned DataFrame
        """
        df_clean = df.copy()
        
        # Remove duplicates
        df_clean = df_clean.drop_duplicates()
        
        # Handle missing values (if any)
        df_clean = df_clean.dropna()
        
        # Ensure correct data types
        for col in NUMERICAL_FEATURES:
            if col in df_clean.columns:
                df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
        
        # Remove any rows with invalid values after conversion
        df_clean = df_clean.dropna()
        
        logger.info(f"Cleaned data: {len(df)} -> {len(df_clean)} records")
        return df_clean
    
    def encode_categorical(self, df: pd.DataFrame, fit: bool = True) -> pd.DataFrame:
        """
        Encode categorical features
        
        Args:
            df: Pandas DataFrame
            fit: Whether to fit encoders (True for training data)
            
        Returns:
            DataFrame with encoded features
        """
        df_encoded = df.copy()
        
        for feature in CATEGORICAL_FEATURES:
            if feature in df_encoded.columns:
                if fit:
                    self.label_encoders[feature] = LabelEncoder()
                    df_encoded[f'{feature}_encoded'] = self.label_encoders[feature].fit_transform(df_encoded[feature])
                else:
                    if feature in self.label_encoders:
                        df_encoded[f'{feature}_encoded'] = self.label_encoders[feature].transform(df_encoded[feature])
        
        return df_encoded
    
    def normalize_features(self, df: pd.DataFrame, features: list = None, fit: bool = True) -> pd.DataFrame:
        """
        Normalize numerical features
        
        Args:
            df: Pandas DataFrame
            features: List of features to normalize (None for all numerical)
            fit: Whether to fit scaler
            
        Returns:
            DataFrame with normalized features
        """
        if features is None:
            features = [f for f in NUMERICAL_FEATURES if f in df.columns]
        
        df_normalized = df.copy()
        
        if fit:
            df_normalized[features] = self.scaler.fit_transform(df[features])
            self.is_fitted = True
        else:
            if self.is_fitted:
                df_normalized[features] = self.scaler.transform(df[features])
        
        return df_normalized
    
    def get_feature_statistics(self, df: pd.DataFrame) -> dict:
        """
        Calculate comprehensive feature statistics
        
        Args:
            df: Pandas DataFrame
            
        Returns:
            Dictionary of statistics
        """
        stats = {}
        
        # Numerical features
        for feature in NUMERICAL_FEATURES:
            if feature in df.columns:
                stats[feature] = {
                    'mean': df[feature].mean(),
                    'median': df[feature].median(),
                    'std': df[feature].std(),
                    'min': df[feature].min(),
                    'max': df[feature].max(),
                    'q25': df[feature].quantile(0.25),
                    'q75': df[feature].quantile(0.75),
                }
        
        # Categorical features
        for feature in CATEGORICAL_FEATURES:
            if feature in df.columns:
                stats[feature] = {
                    'unique_values': df[feature].nunique(),
                    'value_counts': df[feature].value_counts().to_dict(),
                    'mode': df[feature].mode()[0] if len(df[feature].mode()) > 0 else None,
                }
        
        return stats
    
    def create_feature_summary(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create summary table of features
        
        Args:
            df: Pandas DataFrame
            
        Returns:
            Summary DataFrame
        """
        summary_data = []
        
        for col in df.columns:
            summary_data.append({
                'Feature': col,
                'Type': 'Numerical' if col in NUMERICAL_FEATURES else 'Categorical',
                'Missing': df[col].isna().sum(),
                'Unique': df[col].nunique(),
                'Sample': df[col].iloc[0] if len(df) > 0 else None,
            })
        
        return pd.DataFrame(summary_data)

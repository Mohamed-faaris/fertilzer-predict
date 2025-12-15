"""
Analytics engine for comprehensive data analysis
"""
import pandas as pd
import numpy as np
from scipy import stats
import sys
sys.path.append('/home/faaris/projects/BDA/fert-predict')
from config.settings import NUMERICAL_FEATURES, CATEGORICAL_FEATURES
import logging

logger = logging.getLogger(__name__)


class AnalyticsEngine:
    """Comprehensive analytics and insights generation"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize analytics engine
        
        Args:
            df: Pandas DataFrame with fertilizer data
        """
        self.df = df
    
    def analyze_by_crop(self, crop_type: str = None) -> dict:
        """
        Analyze data by crop type
        
        Args:
            crop_type: Specific crop to analyze (None for all)
            
        Returns:
            Dictionary with crop analysis
        """
        if crop_type:
            crop_df = self.df[self.df['Crop Type'] == crop_type]
        else:
            crop_df = self.df
        
        analysis = {
            'total_records': len(crop_df),
            'fertilizer_distribution': crop_df['Fertilizer Name'].value_counts().to_dict(),
            'soil_distribution': crop_df['Soil Type'].value_counts().to_dict(),
            'avg_nutrients': {
                'Nitrogen': crop_df['Nitrogen'].mean(),
                'Potassium': crop_df['Potassium'].mean(),
                'Phosphorous': crop_df['Phosphorous'].mean(),
            },
            'environmental_conditions': {
                'avg_temperature': crop_df['Temparature'].mean(),
                'avg_humidity': crop_df['Humidity'].mean(),
                'avg_moisture': crop_df['Moisture'].mean(),
            },
            'recommended_fertilizers': crop_df['Fertilizer Name'].value_counts().head(3).to_dict(),
        }
        
        return analysis
    
    def analyze_by_soil(self, soil_type: str = None) -> dict:
        """
        Analyze data by soil type
        
        Args:
            soil_type: Specific soil to analyze (None for all)
            
        Returns:
            Dictionary with soil analysis
        """
        if soil_type:
            soil_df = self.df[self.df['Soil Type'] == soil_type]
        else:
            soil_df = self.df
        
        analysis = {
            'total_records': len(soil_df),
            'crop_distribution': soil_df['Crop Type'].value_counts().to_dict(),
            'fertilizer_distribution': soil_df['Fertilizer Name'].value_counts().to_dict(),
            'avg_nutrients': {
                'Nitrogen': soil_df['Nitrogen'].mean(),
                'Potassium': soil_df['Potassium'].mean(),
                'Phosphorous': soil_df['Phosphorous'].mean(),
            },
            'suitable_crops': soil_df['Crop Type'].value_counts().head(5).to_dict(),
        }
        
        return analysis
    
    def analyze_by_fertilizer(self, fertilizer_name: str = None) -> dict:
        """
        Analyze data by fertilizer type
        
        Args:
            fertilizer_name: Specific fertilizer to analyze (None for all)
            
        Returns:
            Dictionary with fertilizer analysis
        """
        if fertilizer_name:
            fert_df = self.df[self.df['Fertilizer Name'] == fertilizer_name]
        else:
            fert_df = self.df
        
        analysis = {
            'total_records': len(fert_df),
            'usage_percentage': (len(fert_df) / len(self.df)) * 100,
            'crop_usage': fert_df['Crop Type'].value_counts().to_dict(),
            'soil_usage': fert_df['Soil Type'].value_counts().to_dict(),
            'avg_nutrient_levels': {
                'Nitrogen': fert_df['Nitrogen'].mean(),
                'Potassium': fert_df['Potassium'].mean(),
                'Phosphorous': fert_df['Phosphorous'].mean(),
            },
            'environmental_range': {
                'temperature': {
                    'min': fert_df['Temparature'].min(),
                    'max': fert_df['Temparature'].max(),
                    'avg': fert_df['Temparature'].mean(),
                },
                'humidity': {
                    'min': fert_df['Humidity'].min(),
                    'max': fert_df['Humidity'].max(),
                    'avg': fert_df['Humidity'].mean(),
                },
                'moisture': {
                    'min': fert_df['Moisture'].min(),
                    'max': fert_df['Moisture'].max(),
                    'avg': fert_df['Moisture'].mean(),
                },
            },
        }
        
        return analysis
    
    def correlation_analysis(self) -> pd.DataFrame:
        """
        Calculate correlation matrix for numerical features
        
        Returns:
            Correlation DataFrame
        """
        numerical_cols = [col for col in NUMERICAL_FEATURES if col in self.df.columns]
        return self.df[numerical_cols].corr()
    
    def nutrient_distribution_analysis(self) -> dict:
        """
        Analyze nutrient distributions across crops and soils
        
        Returns:
            Dictionary with nutrient analysis
        """
        analysis = {
            'by_crop': {},
            'by_soil': {},
            'overall': {},
        }
        
        # Overall nutrient statistics
        for nutrient in ['Nitrogen', 'Potassium', 'Phosphorous']:
            analysis['overall'][nutrient] = {
                'mean': self.df[nutrient].mean(),
                'median': self.df[nutrient].median(),
                'std': self.df[nutrient].std(),
                'min': self.df[nutrient].min(),
                'max': self.df[nutrient].max(),
            }
        
        # By crop
        for crop in self.df['Crop Type'].unique():
            crop_df = self.df[self.df['Crop Type'] == crop]
            analysis['by_crop'][crop] = {
                'Nitrogen': crop_df['Nitrogen'].mean(),
                'Potassium': crop_df['Potassium'].mean(),
                'Phosphorous': crop_df['Phosphorous'].mean(),
            }
        
        # By soil
        for soil in self.df['Soil Type'].unique():
            soil_df = self.df[self.df['Soil Type'] == soil]
            analysis['by_soil'][soil] = {
                'Nitrogen': soil_df['Nitrogen'].mean(),
                'Potassium': soil_df['Potassium'].mean(),
                'Phosphorous': soil_df['Phosphorous'].mean(),
            }
        
        return analysis
    
    def get_top_combinations(self, n: int = 10) -> pd.DataFrame:
        """
        Get top crop-soil-fertilizer combinations
        
        Args:
            n: Number of top combinations to return
            
        Returns:
            DataFrame with top combinations
        """
        combinations = self.df.groupby(['Crop Type', 'Soil Type', 'Fertilizer Name']).size().reset_index(name='Count')
        combinations = combinations.sort_values('Count', ascending=False).head(n)
        return combinations
    
    def environmental_analysis(self) -> dict:
        """
        Analyze environmental factors
        
        Returns:
            Dictionary with environmental analysis
        """
        analysis = {
            'temperature': {
                'distribution': self.df['Temparature'].describe().to_dict(),
                'by_crop': self.df.groupby('Crop Type')['Temparature'].mean().to_dict(),
            },
            'humidity': {
                'distribution': self.df['Humidity'].describe().to_dict(),
                'by_crop': self.df.groupby('Crop Type')['Humidity'].mean().to_dict(),
            },
            'moisture': {
                'distribution': self.df['Moisture'].describe().to_dict(),
                'by_soil': self.df.groupby('Soil Type')['Moisture'].mean().to_dict(),
            },
        }
        
        return analysis
    
    def generate_insights(self) -> list:
        """
        Generate automated insights from data
        
        Returns:
            List of insight strings
        """
        insights = []
        
        # Most common fertilizer
        top_fertilizer = self.df['Fertilizer Name'].value_counts().index[0]
        top_fert_pct = (self.df['Fertilizer Name'].value_counts().iloc[0] / len(self.df)) * 100
        insights.append(f"**{top_fertilizer}** is the most commonly used fertilizer ({top_fert_pct:.1f}% of cases)")
        
        # Most common crop
        top_crop = self.df['Crop Type'].value_counts().index[0]
        insights.append(f"**{top_crop}** is the most frequently grown crop in the dataset")
        
        # Nutrient insights
        avg_n = self.df['Nitrogen'].mean()
        avg_p = self.df['Phosphorous'].mean()
        avg_k = self.df['Potassium'].mean()
        
        if avg_n > avg_p and avg_n > avg_k:
            insights.append(f"**Nitrogen** has the highest average requirement ({avg_n:.1f}) across all crops")
        elif avg_p > avg_n and avg_p > avg_k:
            insights.append(f"**Phosphorous** has the highest average requirement ({avg_p:.1f}) across all crops")
        else:
            insights.append(f"**Potassium** has the highest average requirement ({avg_k:.1f}) across all crops")
        
        # Temperature range
        temp_range = self.df['Temparature'].max() - self.df['Temparature'].min()
        insights.append(f"Temperature ranges from **{self.df['Temparature'].min()}°C** to **{self.df['Temparature'].max()}°C** (range: {temp_range}°C)")
        
        # Soil diversity
        soil_count = self.df['Soil Type'].nunique()
        insights.append(f"Dataset covers **{soil_count} different soil types** with varying characteristics")
        
        return insights

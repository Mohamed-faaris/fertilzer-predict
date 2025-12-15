"""
Intelligent fertilizer recommendation engine
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import sys
sys.path.append('/home/faaris/projects/BDA/fert-predict')
from config.settings import FERTILIZER_TYPES
import logging

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """Intelligent fertilizer recommendation system"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize recommendation engine
        
        Args:
            df: Historical fertilizer data
        """
        self.df = df
        self._build_knowledge_base()
    
    def _build_knowledge_base(self):
        """Build knowledge base from historical data"""
        # Create lookup tables for quick recommendations
        self.crop_soil_fertilizer = self.df.groupby(['Crop Type', 'Soil Type', 'Fertilizer Name']).size().reset_index(name='frequency')
        self.crop_soil_fertilizer = self.crop_soil_fertilizer.sort_values('frequency', ascending=False)
        
        # Average conditions for each fertilizer
        self.fertilizer_profiles = {}
        for fertilizer in FERTILIZER_TYPES:
            fert_df = self.df[self.df['Fertilizer Name'] == fertilizer]
            if len(fert_df) > 0:
                self.fertilizer_profiles[fertilizer] = {
                    'avg_temperature': fert_df['Temparature'].mean(),
                    'avg_humidity': fert_df['Humidity'].mean(),
                    'avg_moisture': fert_df['Moisture'].mean(),
                    'avg_nitrogen': fert_df['Nitrogen'].mean(),
                    'avg_potassium': fert_df['Potassium'].mean(),
                    'avg_phosphorous': fert_df['Phosphorous'].mean(),
                    'std_temperature': fert_df['Temparature'].std(),
                    'std_humidity': fert_df['Humidity'].std(),
                    'std_moisture': fert_df['Moisture'].std(),
                }
    
    def recommend(self, 
                  temperature: float,
                  humidity: float,
                  moisture: float,
                  soil_type: str,
                  crop_type: str,
                  nitrogen: float = None,
                  potassium: float = None,
                  phosphorous: float = None) -> Dict:
        """
        Recommend fertilizer based on input parameters
        
        Args:
            temperature: Temperature in Celsius
            humidity: Humidity percentage
            moisture: Moisture percentage
            soil_type: Type of soil
            crop_type: Type of crop
            nitrogen: Current nitrogen level (optional)
            potassium: Current potassium level (optional)
            phosphorous: Current phosphorous level (optional)
            
        Returns:
            Dictionary with recommendations
        """
        # Method 1: Rule-based recommendation using crop-soil combination
        rule_based = self._rule_based_recommendation(crop_type, soil_type)
        
        # Method 2: Similarity-based recommendation
        similarity_based = self._similarity_based_recommendation(
            temperature, humidity, moisture, soil_type, crop_type,
            nitrogen, potassium, phosphorous
        )
        
        # Combine recommendations
        primary_recommendation = rule_based[0] if rule_based else similarity_based[0]
        
        # Calculate confidence score
        confidence = self._calculate_confidence(
            primary_recommendation, temperature, humidity, moisture,
            soil_type, crop_type
        )
        
        # Get nutrient analysis
        nutrient_analysis = self._analyze_nutrients(
            primary_recommendation, nitrogen, potassium, phosphorous
        )
        
        # Alternative recommendations
        alternatives = []
        for rec in (rule_based + similarity_based):
            if rec != primary_recommendation and rec not in alternatives:
                alternatives.append(rec)
                if len(alternatives) >= 2:
                    break
        
        return {
            'primary_recommendation': primary_recommendation,
            'confidence_score': confidence,
            'alternatives': alternatives,
            'nutrient_analysis': nutrient_analysis,
            'explanation': self._generate_explanation(
                primary_recommendation, crop_type, soil_type, confidence
            ),
        }
    
    def _rule_based_recommendation(self, crop_type: str, soil_type: str) -> List[str]:
        """
        Get recommendations based on crop-soil combination
        
        Args:
            crop_type: Type of crop
            soil_type: Type of soil
            
        Returns:
            List of recommended fertilizers
        """
        matches = self.crop_soil_fertilizer[
            (self.crop_soil_fertilizer['Crop Type'] == crop_type) &
            (self.crop_soil_fertilizer['Soil Type'] == soil_type)
        ]
        
        if len(matches) > 0:
            return matches['Fertilizer Name'].tolist()[:3]
        
        # Fallback to crop only
        crop_matches = self.df[self.df['Crop Type'] == crop_type]['Fertilizer Name'].value_counts()
        return crop_matches.index.tolist()[:3]
    
    def _similarity_based_recommendation(self,
                                        temperature: float,
                                        humidity: float,
                                        moisture: float,
                                        soil_type: str,
                                        crop_type: str,
                                        nitrogen: float = None,
                                        potassium: float = None,
                                        phosphorous: float = None) -> List[str]:
        """
        Find similar cases and recommend fertilizers
        
        Returns:
            List of recommended fertilizers
        """
        # Filter by crop and soil
        similar_df = self.df[
            (self.df['Crop Type'] == crop_type) &
            (self.df['Soil Type'] == soil_type)
        ].copy()
        
        if len(similar_df) == 0:
            similar_df = self.df[self.df['Crop Type'] == crop_type].copy()
        
        if len(similar_df) == 0:
            return []
        
        # Calculate similarity based on environmental factors
        similar_df['similarity'] = (
            np.abs(similar_df['Temparature'] - temperature) +
            np.abs(similar_df['Humidity'] - humidity) +
            np.abs(similar_df['Moisture'] - moisture)
        )
        
        # Sort by similarity
        similar_df = similar_df.sort_values('similarity')
        
        # Get top fertilizers
        top_fertilizers = similar_df.head(10)['Fertilizer Name'].value_counts()
        return top_fertilizers.index.tolist()[:3]
    
    def _calculate_confidence(self,
                             fertilizer: str,
                             temperature: float,
                             humidity: float,
                             moisture: float,
                             soil_type: str,
                             crop_type: str) -> float:
        """
        Calculate confidence score for recommendation
        
        Returns:
            Confidence score between 0 and 1
        """
        if fertilizer not in self.fertilizer_profiles:
            return 0.5
        
        profile = self.fertilizer_profiles[fertilizer]
        
        # Calculate how well input matches typical profile
        temp_diff = abs(temperature - profile['avg_temperature']) / (profile['std_temperature'] + 1)
        humidity_diff = abs(humidity - profile['avg_humidity']) / (profile['std_humidity'] + 1)
        moisture_diff = abs(moisture - profile['avg_moisture']) / (profile['std_moisture'] + 1)
        
        # Average difference (lower is better)
        avg_diff = (temp_diff + humidity_diff + moisture_diff) / 3
        
        # Convert to confidence (0-1 scale)
        confidence = max(0.0, min(1.0, 1.0 - (avg_diff / 3)))
        
        # Boost confidence if crop-soil combination is common
        combo_count = len(self.crop_soil_fertilizer[
            (self.crop_soil_fertilizer['Crop Type'] == crop_type) &
            (self.crop_soil_fertilizer['Soil Type'] == soil_type) &
            (self.crop_soil_fertilizer['Fertilizer Name'] == fertilizer)
        ])
        
        if combo_count > 10:
            confidence = min(1.0, confidence + 0.1)
        
        return round(confidence, 2)
    
    def _analyze_nutrients(self,
                          fertilizer: str,
                          nitrogen: float = None,
                          potassium: float = None,
                          phosphorous: float = None) -> Dict:
        """
        Analyze nutrient requirements
        
        Returns:
            Dictionary with nutrient analysis
        """
        if fertilizer not in self.fertilizer_profiles:
            return {}
        
        profile = self.fertilizer_profiles[fertilizer]
        
        analysis = {
            'expected_nitrogen': round(profile['avg_nitrogen'], 1),
            'expected_potassium': round(profile['avg_potassium'], 1),
            'expected_phosphorous': round(profile['avg_phosphorous'], 1),
        }
        
        if nitrogen is not None:
            analysis['nitrogen_status'] = 'adequate' if nitrogen >= profile['avg_nitrogen'] * 0.8 else 'deficient'
        
        if potassium is not None:
            analysis['potassium_status'] = 'adequate' if potassium >= profile['avg_potassium'] * 0.8 else 'deficient'
        
        if phosphorous is not None:
            analysis['phosphorous_status'] = 'adequate' if phosphorous >= profile['avg_phosphorous'] * 0.8 else 'deficient'
        
        return analysis
    
    def _generate_explanation(self,
                             fertilizer: str,
                             crop_type: str,
                             soil_type: str,
                             confidence: float) -> str:
        """
        Generate human-readable explanation
        
        Returns:
            Explanation string
        """
        # Count occurrences
        count = len(self.df[
            (self.df['Crop Type'] == crop_type) &
            (self.df['Soil Type'] == soil_type) &
            (self.df['Fertilizer Name'] == fertilizer)
        ])
        
        explanation = f"**{fertilizer}** is recommended for **{crop_type}** grown in **{soil_type}** soil. "
        
        if count > 0:
            explanation += f"This combination appears {count} times in our historical data. "
        
        if confidence >= 0.8:
            explanation += "We have high confidence in this recommendation based on similar environmental conditions."
        elif confidence >= 0.6:
            explanation += "This recommendation is based on moderately similar conditions in our database."
        else:
            explanation += "This is a tentative recommendation. Consider consulting with an agricultural expert."
        
        return explanation
    
    def batch_recommend(self, input_df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate recommendations for multiple inputs
        
        Args:
            input_df: DataFrame with input parameters
            
        Returns:
            DataFrame with recommendations
        """
        results = []
        
        for idx, row in input_df.iterrows():
            rec = self.recommend(
                temperature=row.get('Temparature', row.get('Temperature', 30)),
                humidity=row.get('Humidity', 60),
                moisture=row.get('Moisture', 40),
                soil_type=row.get('Soil Type', 'Loamy'),
                crop_type=row.get('Crop Type', 'Wheat'),
                nitrogen=row.get('Nitrogen'),
                potassium=row.get('Potassium'),
                phosphorous=row.get('Phosphorous'),
            )
            
            results.append({
                'Input_Index': idx,
                'Recommended_Fertilizer': rec['primary_recommendation'],
                'Confidence': rec['confidence_score'],
                'Alternative_1': rec['alternatives'][0] if len(rec['alternatives']) > 0 else None,
                'Alternative_2': rec['alternatives'][1] if len(rec['alternatives']) > 1 else None,
            })
        
        return pd.DataFrame(results)

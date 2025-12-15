"""
Analysis page - Detailed multi-dimensional analysis
"""
import streamlit as st
import pandas as pd
import sys
sys.path.append('/home/faaris/projects/BDA/fert-predict')
from src.backend.spark_engine import spark_engine
from src.backend.analytics_engine import AnalyticsEngine
from src.frontend.components.charts import create_bar_chart, create_horizontal_bar_chart
from src.utils.helpers import format_number, format_percentage
from config.settings import MAIN_DATA_FILE, CROP_TYPES, SOIL_TYPES, FERTILIZER_TYPES


@st.cache_data
def load_analysis_data():
    """Load and cache data for analysis"""
    spark_df = spark_engine.load_data(str(MAIN_DATA_FILE))
    df = spark_engine.to_pandas(spark_df)
    return df


def show():
    """Display analysis page"""
    st.title("📈 Detailed Analysis")
    st.markdown("Explore data across multiple dimensions")
    st.markdown("---")
    
    # Load data
    with st.spinner("Loading data..."):
        df = load_analysis_data()
        analytics = AnalyticsEngine(df)
    
    # Analysis dimension selector
    analysis_type = st.selectbox(
        "Select Analysis Dimension",
        ["By Crop Type", "By Soil Type", "By Fertilizer", "Nutrient Analysis", "Environmental Analysis"]
    )
    
    st.markdown("---")
    
    if analysis_type == "By Crop Type":
        show_crop_analysis(df, analytics)
    elif analysis_type == "By Soil Type":
        show_soil_analysis(df, analytics)
    elif analysis_type == "By Fertilizer":
        show_fertilizer_analysis(df, analytics)
    elif analysis_type == "Nutrient Analysis":
        show_nutrient_analysis(df, analytics)
    elif analysis_type == "Environmental Analysis":
        show_environmental_analysis(df, analytics)


def show_crop_analysis(df, analytics):
    """Show crop-based analysis"""
    st.subheader("🌱 Analysis by Crop Type")
    
    # Crop selector
    selected_crop = st.selectbox("Select Crop", ["All Crops"] + sorted(CROP_TYPES))
    
    if selected_crop == "All Crops":
        crop_analysis = analytics.analyze_by_crop()
    else:
        crop_analysis = analytics.analyze_by_crop(selected_crop)
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Records", format_number(crop_analysis['total_records'], 0))
    
    with col2:
        top_fert = list(crop_analysis['recommended_fertilizers'].keys())[0]
        st.metric("Top Fertilizer", top_fert)
    
    with col3:
        top_soil = list(crop_analysis['soil_distribution'].keys())[0]
        st.metric("Preferred Soil", top_soil)
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Fertilizer Distribution**")
        fert_series = pd.Series(crop_analysis['fertilizer_distribution'])
        fig = create_horizontal_bar_chart(
            fert_series,
            f"Fertilizers for {selected_crop}",
            "Count",
            "Fertilizer",
            color="#4CAF50"
        )
        st.pyplot(fig)
    
    with col2:
        st.write("**Soil Distribution**")
        soil_series = pd.Series(crop_analysis['soil_distribution'])
        fig = create_horizontal_bar_chart(
            soil_series,
            f"Soil Types for {selected_crop}",
            "Count",
            "Soil Type",
            color="#FF9800"
        )
        st.pyplot(fig)
    
    # Nutrient requirements
    st.markdown("---")
    st.subheader("💊 Average Nutrient Requirements")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Nitrogen", f"{crop_analysis['avg_nutrients']['Nitrogen']:.1f}")
    
    with col2:
        st.metric("Potassium", f"{crop_analysis['avg_nutrients']['Potassium']:.1f}")
    
    with col3:
        st.metric("Phosphorous", f"{crop_analysis['avg_nutrients']['Phosphorous']:.1f}")
    
    # Environmental conditions
    st.markdown("---")
    st.subheader("🌡️ Optimal Environmental Conditions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Temperature", f"{crop_analysis['environmental_conditions']['avg_temperature']:.1f}°C")
    
    with col2:
        st.metric("Humidity", f"{crop_analysis['environmental_conditions']['avg_humidity']:.1f}%")
    
    with col3:
        st.metric("Moisture", f"{crop_analysis['environmental_conditions']['avg_moisture']:.1f}%")


def show_soil_analysis(df, analytics):
    """Show soil-based analysis"""
    st.subheader("🌍 Analysis by Soil Type")
    
    # Soil selector
    selected_soil = st.selectbox("Select Soil Type", ["All Soils"] + sorted(SOIL_TYPES))
    
    if selected_soil == "All Soils":
        soil_analysis = analytics.analyze_by_soil()
    else:
        soil_analysis = analytics.analyze_by_soil(selected_soil)
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Records", format_number(soil_analysis['total_records'], 0))
    
    with col2:
        top_crop = list(soil_analysis['suitable_crops'].keys())[0]
        st.metric("Top Crop", top_crop)
    
    with col3:
        top_fert = list(soil_analysis['fertilizer_distribution'].keys())[0]
        st.metric("Top Fertilizer", top_fert)
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Suitable Crops**")
        crop_series = pd.Series(soil_analysis['suitable_crops'])
        fig = create_horizontal_bar_chart(
            crop_series,
            f"Top Crops for {selected_soil} Soil",
            "Count",
            "Crop",
            color="#8BC34A"
        )
        st.pyplot(fig)
    
    with col2:
        st.write("**Fertilizer Usage**")
        fert_series = pd.Series(soil_analysis['fertilizer_distribution']).head(7)
        fig = create_horizontal_bar_chart(
            fert_series,
            f"Fertilizers for {selected_soil} Soil",
            "Count",
            "Fertilizer",
            color="#2196F3"
        )
        st.pyplot(fig)
    
    # Nutrient levels
    st.markdown("---")
    st.subheader("💊 Average Nutrient Levels")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Nitrogen", f"{soil_analysis['avg_nutrients']['Nitrogen']:.1f}")
    
    with col2:
        st.metric("Potassium", f"{soil_analysis['avg_nutrients']['Potassium']:.1f}")
    
    with col3:
        st.metric("Phosphorous", f"{soil_analysis['avg_nutrients']['Phosphorous']:.1f}")


def show_fertilizer_analysis(df, analytics):
    """Show fertilizer-based analysis"""
    st.subheader("🧪 Analysis by Fertilizer Type")
    
    # Fertilizer selector
    selected_fert = st.selectbox("Select Fertilizer", ["All Fertilizers"] + sorted(FERTILIZER_TYPES))
    
    if selected_fert == "All Fertilizers":
        fert_analysis = analytics.analyze_by_fertilizer()
    else:
        fert_analysis = analytics.analyze_by_fertilizer(selected_fert)
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Usage", format_number(fert_analysis['total_records'], 0))
    
    with col2:
        st.metric("Usage %", format_percentage(fert_analysis['usage_percentage']))
    
    with col3:
        top_crop = list(fert_analysis['crop_usage'].keys())[0]
        st.metric("Top Crop", top_crop)
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Crop Usage**")
        crop_series = pd.Series(fert_analysis['crop_usage']).head(8)
        fig = create_horizontal_bar_chart(
            crop_series,
            f"Crops using {selected_fert}",
            "Count",
            "Crop",
            color="#9C27B0"
        )
        st.pyplot(fig)
    
    with col2:
        st.write("**Soil Usage**")
        soil_series = pd.Series(fert_analysis['soil_usage'])
        fig = create_horizontal_bar_chart(
            soil_series,
            f"Soil Types using {selected_fert}",
            "Count",
            "Soil",
            color="#FF5722"
        )
        st.pyplot(fig)
    
    # Environmental ranges
    st.markdown("---")
    st.subheader("🌡️ Optimal Environmental Ranges")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        temp_range = fert_analysis['environmental_range']['temperature']
        st.metric(
            "Temperature",
            f"{temp_range['avg']:.1f}°C",
            delta=f"Range: {temp_range['min']:.0f}-{temp_range['max']:.0f}°C"
        )
    
    with col2:
        hum_range = fert_analysis['environmental_range']['humidity']
        st.metric(
            "Humidity",
            f"{hum_range['avg']:.1f}%",
            delta=f"Range: {hum_range['min']:.0f}-{hum_range['max']:.0f}%"
        )
    
    with col3:
        moist_range = fert_analysis['environmental_range']['moisture']
        st.metric(
            "Moisture",
            f"{moist_range['avg']:.1f}%",
            delta=f"Range: {moist_range['min']:.0f}-{moist_range['max']:.0f}%"
        )


def show_nutrient_analysis(df, analytics):
    """Show nutrient analysis"""
    st.subheader("💊 Nutrient Distribution Analysis")
    
    nutrient_data = analytics.nutrient_distribution_analysis()
    
    # Overall statistics
    st.write("**Overall Nutrient Statistics**")
    
    nutrient_df = pd.DataFrame(nutrient_data['overall']).T
    st.dataframe(nutrient_df, use_container_width=True)
    
    st.markdown("---")
    
    # By crop
    st.write("**Average Nutrients by Crop**")
    crop_nutrients = pd.DataFrame(nutrient_data['by_crop']).T
    st.dataframe(crop_nutrients, use_container_width=True)
    
    st.markdown("---")
    
    # By soil
    st.write("**Average Nutrients by Soil**")
    soil_nutrients = pd.DataFrame(nutrient_data['by_soil']).T
    st.dataframe(soil_nutrients, use_container_width=True)


def show_environmental_analysis(df, analytics):
    """Show environmental analysis"""
    st.subheader("🌡️ Environmental Factors Analysis")
    
    env_data = analytics.environmental_analysis()
    
    # Temperature analysis
    st.write("**Temperature Distribution**")
    temp_df = pd.DataFrame(env_data['temperature']['distribution'], index=[0])
    st.dataframe(temp_df, use_container_width=True)
    
    st.write("**Average Temperature by Crop**")
    temp_crop = pd.Series(env_data['temperature']['by_crop']).sort_values(ascending=False)
    fig = create_horizontal_bar_chart(
        temp_crop,
        "Average Temperature by Crop",
        "Temperature (°C)",
        "Crop",
        color="#FF5722"
    )
    st.pyplot(fig)
    
    st.markdown("---")
    
    # Humidity analysis
    st.write("**Humidity Distribution**")
    hum_df = pd.DataFrame(env_data['humidity']['distribution'], index=[0])
    st.dataframe(hum_df, use_container_width=True)
    
    st.markdown("---")
    
    # Moisture analysis
    st.write("**Moisture Distribution**")
    moist_df = pd.DataFrame(env_data['moisture']['distribution'], index=[0])
    st.dataframe(moist_df, use_container_width=True)
    
    st.write("**Average Moisture by Soil Type**")
    moist_soil = pd.Series(env_data['moisture']['by_soil']).sort_values(ascending=False)
    fig = create_horizontal_bar_chart(
        moist_soil,
        "Average Moisture by Soil",
        "Moisture (%)",
        "Soil Type",
        color="#00BCD4"
    )
    st.pyplot(fig)

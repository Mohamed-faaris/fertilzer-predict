"""
Dashboard page - Key metrics and overview
"""
import streamlit as st
import pandas as pd
import sys
sys.path.append('/home/faaris/projects/BDA/fert-predict')
from src.backend.spark_engine import spark_engine
from src.backend.analytics_engine import AnalyticsEngine
from src.frontend.components.charts import create_pie_chart, create_bar_chart
from src.utils.helpers import format_number, get_fertilizer_colors_list, get_soil_colors_list
from config.settings import MAIN_DATA_FILE


@st.cache_data
def load_dashboard_data():
    """Load and cache data for dashboard"""
    spark_df = spark_engine.load_data(str(MAIN_DATA_FILE))
    df = spark_engine.to_pandas(spark_df)
    return df


def show():
    """Display dashboard page"""
    st.title("🏠 Dashboard - Key Metrics & Overview")
    st.markdown("---")
    
    # Load data
    with st.spinner("Loading data..."):
        df = load_dashboard_data()
        analytics = AnalyticsEngine(df)
    
    # Key Metrics Row
    st.subheader("📊 Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Records",
            value=format_number(len(df), 0),
            delta="100K+ Dataset"
        )
    
    with col2:
        st.metric(
            label="Crop Types",
            value=df['Crop Type'].nunique(),
            delta=f"{df['Crop Type'].mode()[0]} (Most Common)"
        )
    
    with col3:
        st.metric(
            label="Soil Types",
            value=df['Soil Type'].nunique(),
            delta=f"{df['Soil Type'].mode()[0]} (Most Common)"
        )
    
    with col4:
        st.metric(
            label="Fertilizer Types",
            value=df['Fertilizer Name'].nunique(),
            delta=f"{df['Fertilizer Name'].mode()[0]} (Most Used)"
        )
    
    st.markdown("---")
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌾 Fertilizer Distribution")
        fert_dist = df['Fertilizer Name'].value_counts()
        fig = create_pie_chart(
            fert_dist,
            "Fertilizer Usage Distribution",
            colors=get_fertilizer_colors_list()
        )
        st.pyplot(fig)
    
    with col2:
        st.subheader("🌍 Soil Type Distribution")
        soil_dist = df['Soil Type'].value_counts()
        fig = create_pie_chart(
            soil_dist,
            "Soil Type Distribution",
            colors=get_soil_colors_list()
        )
        st.pyplot(fig)
    
    st.markdown("---")
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌱 Top 10 Crops")
        crop_dist = df['Crop Type'].value_counts().head(10)
        fig = create_bar_chart(
            crop_dist,
            "Top 10 Crops by Frequency",
            "Crop Type",
            "Count",
            color="#4CAF50"
        )
        st.pyplot(fig)
    
    with col2:
        st.subheader("💧 Average Nutrient Levels")
        nutrient_data = pd.Series({
            'Nitrogen': df['Nitrogen'].mean(),
            'Potassium': df['Potassium'].mean(),
            'Phosphorous': df['Phosphorous'].mean()
        })
        fig = create_bar_chart(
            nutrient_data,
            "Average Nutrient Requirements",
            "Nutrient",
            "Average Level",
            color="#2196F3"
        )
        st.pyplot(fig)
    
    st.markdown("---")
    
    # Environmental Conditions
    st.subheader("🌡️ Environmental Conditions Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Avg Temperature",
            value=f"{df['Temparature'].mean():.1f}°C",
            delta=f"Range: {df['Temparature'].min():.0f}-{df['Temparature'].max():.0f}°C"
        )
    
    with col2:
        st.metric(
            label="Avg Humidity",
            value=f"{df['Humidity'].mean():.1f}%",
            delta=f"Range: {df['Humidity'].min():.0f}-{df['Humidity'].max():.0f}%"
        )
    
    with col3:
        st.metric(
            label="Avg Moisture",
            value=f"{df['Moisture'].mean():.1f}%",
            delta=f"Range: {df['Moisture'].min():.0f}-{df['Moisture'].max():.0f}%"
        )
    
    st.markdown("---")
    
    # Quick Insights
    st.subheader("💡 Quick Insights")
    insights = analytics.generate_insights()
    
    for i, insight in enumerate(insights, 1):
        st.markdown(f"{i}. {insight}")
    
    st.markdown("---")
    
    # Top Combinations
    st.subheader("🏆 Top Crop-Soil-Fertilizer Combinations")
    top_combos = analytics.get_top_combinations(10)
    
    # Display as table
    st.dataframe(
        top_combos,
        use_container_width=True,
        hide_index=True
    )
    
    # Data Summary
    st.markdown("---")
    st.subheader("📋 Dataset Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Numerical Features Summary:**")
        st.dataframe(
            df[['Temparature', 'Humidity', 'Moisture', 'Nitrogen', 'Potassium', 'Phosphorous']].describe(),
            use_container_width=True
        )
    
    with col2:
        st.write("**Categorical Features:**")
        cat_summary = pd.DataFrame({
            'Feature': ['Crop Type', 'Soil Type', 'Fertilizer Name'],
            'Unique Values': [
                df['Crop Type'].nunique(),
                df['Soil Type'].nunique(),
                df['Fertilizer Name'].nunique()
            ],
            'Most Common': [
                df['Crop Type'].mode()[0],
                df['Soil Type'].mode()[0],
                df['Fertilizer Name'].mode()[0]
            ]
        })
        st.dataframe(cat_summary, use_container_width=True, hide_index=True)

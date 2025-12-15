"""
Reports page - Executive summary reports and insights
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import sys
sys.path.append('/home/faaris/projects/BDA/fert-predict')
from src.backend.spark_engine import spark_engine
from src.backend.analytics_engine import AnalyticsEngine
from src.backend.data_processor import DataProcessor
from src.utils.helpers import format_number, create_download_filename
from config.settings import MAIN_DATA_FILE


@st.cache_data
def load_report_data():
    """Load and cache data for reports"""
    spark_df = spark_engine.load_data(str(MAIN_DATA_FILE))
    df = spark_engine.to_pandas(spark_df)
    return df


def show():
    """Display reports page"""
    st.title("📄 Executive Reports & Insights")
    st.markdown("Automated summary reports with actionable recommendations")
    st.markdown("---")
    
    # Load data
    with st.spinner("Generating reports..."):
        df = load_report_data()
        analytics = AnalyticsEngine(df)
        processor = DataProcessor()
    
    # Report type selector
    report_type = st.selectbox(
        "Select Report Type",
        [
            "Executive Summary",
            "Data Quality Report",
            "Crop Performance Report",
            "Fertilizer Usage Report",
            "Environmental Analysis Report"
        ]
    )
    
    st.markdown("---")
    
    if report_type == "Executive Summary":
        show_executive_summary(df, analytics)
    elif report_type == "Data Quality Report":
        show_data_quality_report(df, processor)
    elif report_type == "Crop Performance Report":
        show_crop_performance_report(df, analytics)
    elif report_type == "Fertilizer Usage Report":
        show_fertilizer_usage_report(df, analytics)
    elif report_type == "Environmental Analysis Report":
        show_environmental_report(df, analytics)


def show_executive_summary(df, analytics):
    """Show executive summary report"""
    st.subheader("📊 Executive Summary Report")
    st.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    st.markdown("---")
    
    # Overview
    st.write("### 📈 Dataset Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", format_number(len(df), 0))
    
    with col2:
        st.metric("Crop Varieties", df['Crop Type'].nunique())
    
    with col3:
        st.metric("Soil Types", df['Soil Type'].nunique())
    
    with col4:
        st.metric("Fertilizer Types", df['Fertilizer Name'].nunique())
    
    st.markdown("---")
    
    # Key Insights
    st.write("### 💡 Key Insights")
    insights = analytics.generate_insights()
    
    for i, insight in enumerate(insights, 1):
        st.markdown(f"**{i}.** {insight}")
    
    st.markdown("---")
    
    # Top Performers
    st.write("### 🏆 Top Performers")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Most Common Crops:**")
        top_crops = df['Crop Type'].value_counts().head(5)
        for crop, count in top_crops.items():
            pct = (count / len(df)) * 100
            st.write(f"- {crop}: {format_number(count, 0)} ({pct:.1f}%)")
    
    with col2:
        st.write("**Most Used Fertilizers:**")
        top_ferts = df['Fertilizer Name'].value_counts().head(5)
        for fert, count in top_ferts.items():
            pct = (count / len(df)) * 100
            st.write(f"- {fert}: {format_number(count, 0)} ({pct:.1f}%)")
    
    st.markdown("---")
    
    # Recommendations
    st.write("### 🎯 Strategic Recommendations")
    
    st.success("""
    **1. Optimize Fertilizer Inventory**
    - Focus on top 3 fertilizers which cover 60%+ of use cases
    - Maintain adequate stock of Urea, DAP, and 28-28 formulations
    """)
    
    st.info("""
    **2. Crop-Soil Matching**
    - Promote optimal crop-soil combinations based on historical data
    - Provide guidance for farmers on best practices
    """)
    
    st.warning("""
    **3. Environmental Monitoring**
    - Implement real-time monitoring for temperature and humidity
    - Adjust fertilizer recommendations based on seasonal variations
    """)


def show_data_quality_report(df, processor):
    """Show data quality report"""
    st.subheader("🔍 Data Quality Report")
    
    # Validate data
    validation = processor.validate_data(df)
    
    # Overall quality score
    total_issues = (
        len(validation['missing_values']) +
        len(validation['invalid_values']) +
        validation['duplicates']
    )
    
    quality_score = max(0, 100 - (total_issues / len(df) * 100))
    
    st.metric("Data Quality Score", f"{quality_score:.1f}%")
    
    st.markdown("---")
    
    # Missing values
    st.write("### ❌ Missing Values")
    if validation['missing_values']:
        missing_df = pd.DataFrame([
            {'Column': col, 'Missing Count': count, 'Percentage': f"{(count/len(df)*100):.2f}%"}
            for col, count in validation['missing_values'].items()
        ])
        st.dataframe(missing_df, use_container_width=True, hide_index=True)
    else:
        st.success("✅ No missing values detected")
    
    st.markdown("---")
    
    # Invalid values
    st.write("### ⚠️ Invalid Values")
    if validation['invalid_values']:
        for col, values in validation['invalid_values'].items():
            st.warning(f"**{col}:** {', '.join(map(str, values))}")
    else:
        st.success("✅ No invalid values detected")
    
    st.markdown("---")
    
    # Duplicates
    st.write("### 🔄 Duplicate Records")
    if validation['duplicates'] > 0:
        st.warning(f"Found {validation['duplicates']} duplicate records ({(validation['duplicates']/len(df)*100):.2f}%)")
    else:
        st.success("✅ No duplicate records found")
    
    st.markdown("---")
    
    # Data types
    st.write("### 📋 Data Types")
    dtype_df = pd.DataFrame([
        {'Column': col, 'Data Type': dtype}
        for col, dtype in validation['data_types'].items()
    ])
    st.dataframe(dtype_df, use_container_width=True, hide_index=True)


def show_crop_performance_report(df, analytics):
    """Show crop performance report"""
    st.subheader("🌱 Crop Performance Report")
    
    # Crop statistics
    crop_stats = []
    
    for crop in df['Crop Type'].unique():
        crop_data = analytics.analyze_by_crop(crop)
        crop_stats.append({
            'Crop': crop,
            'Records': crop_data['total_records'],
            'Avg Nitrogen': f"{crop_data['avg_nutrients']['Nitrogen']:.1f}",
            'Avg Potassium': f"{crop_data['avg_nutrients']['Potassium']:.1f}",
            'Avg Phosphorous': f"{crop_data['avg_nutrients']['Phosphorous']:.1f}",
            'Top Fertilizer': list(crop_data['recommended_fertilizers'].keys())[0],
            'Preferred Soil': list(crop_data['soil_distribution'].keys())[0],
        })
    
    crop_df = pd.DataFrame(crop_stats).sort_values('Records', ascending=False)
    st.dataframe(crop_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Download option
    csv = crop_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Crop Performance Report (CSV)",
        data=csv,
        file_name=create_download_filename("crop_performance_report"),
        mime="text/csv"
    )


def show_fertilizer_usage_report(df, analytics):
    """Show fertilizer usage report"""
    st.subheader("🧪 Fertilizer Usage Report")
    
    # Fertilizer statistics
    fert_stats = []
    
    for fert in df['Fertilizer Name'].unique():
        fert_data = analytics.analyze_by_fertilizer(fert)
        fert_stats.append({
            'Fertilizer': fert,
            'Usage Count': fert_data['total_records'],
            'Usage %': f"{fert_data['usage_percentage']:.1f}%",
            'Top Crop': list(fert_data['crop_usage'].keys())[0],
            'Top Soil': list(fert_data['soil_usage'].keys())[0],
            'Avg Temp': f"{fert_data['environmental_range']['temperature']['avg']:.1f}°C",
            'Avg Humidity': f"{fert_data['environmental_range']['humidity']['avg']:.1f}%",
        })
    
    fert_df = pd.DataFrame(fert_stats).sort_values('Usage Count', ascending=False)
    st.dataframe(fert_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Recommendations
    st.write("### 📌 Fertilizer Recommendations")
    
    top_3 = fert_df.head(3)
    total_coverage = sum([int(row['Usage Count']) for _, row in top_3.iterrows()])
    coverage_pct = (total_coverage / len(df)) * 100
    
    st.info(f"""
    **Inventory Optimization:**
    - Top 3 fertilizers ({', '.join(top_3['Fertilizer'].tolist())}) cover {coverage_pct:.1f}% of all use cases
    - Prioritize stock management for these fertilizers
    - Consider seasonal demand patterns
    """)
    
    # Download option
    csv = fert_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Fertilizer Usage Report (CSV)",
        data=csv,
        file_name=create_download_filename("fertilizer_usage_report"),
        mime="text/csv"
    )


def show_environmental_report(df, analytics):
    """Show environmental analysis report"""
    st.subheader("🌡️ Environmental Analysis Report")
    
    env_data = analytics.environmental_analysis()
    
    # Temperature analysis
    st.write("### 🌡️ Temperature Analysis")
    temp_stats = pd.DataFrame(env_data['temperature']['distribution'], index=['Value']).T
    st.dataframe(temp_stats, use_container_width=True)
    
    st.markdown("---")
    
    # Humidity analysis
    st.write("### 💧 Humidity Analysis")
    hum_stats = pd.DataFrame(env_data['humidity']['distribution'], index=['Value']).T
    st.dataframe(hum_stats, use_container_width=True)
    
    st.markdown("---")
    
    # Moisture analysis
    st.write("### 🌊 Moisture Analysis")
    moist_stats = pd.DataFrame(env_data['moisture']['distribution'], index=['Value']).T
    st.dataframe(moist_stats, use_container_width=True)
    
    st.markdown("---")
    
    # Environmental recommendations
    st.write("### 🎯 Environmental Recommendations")
    
    avg_temp = env_data['temperature']['distribution']['mean']
    avg_hum = env_data['humidity']['distribution']['mean']
    avg_moist = env_data['moisture']['distribution']['mean']
    
    st.success(f"""
    **Optimal Conditions:**
    - Temperature: {avg_temp:.1f}°C (±5°C tolerance)
    - Humidity: {avg_hum:.1f}% (±10% tolerance)
    - Moisture: {avg_moist:.1f}% (±10% tolerance)
    
    Monitor and maintain these conditions for optimal crop growth and fertilizer effectiveness.
    """)

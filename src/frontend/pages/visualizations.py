"""
Visualizations page - Interactive charts and graphs
"""
import streamlit as st
import pandas as pd
import sys
sys.path.append('/home/faaris/projects/BDA/fert-predict')
from src.backend.spark_engine import spark_engine
from src.backend.analytics_engine import AnalyticsEngine
from src.frontend.components.charts import (
    create_correlation_heatmap, create_box_plot, create_scatter_plot,
    create_distribution_plot, create_grouped_bar_chart
)
from config.settings import MAIN_DATA_FILE, NUMERICAL_FEATURES


@st.cache_data
def load_viz_data():
    """Load and cache data for visualizations"""
    spark_df = spark_engine.load_data(str(MAIN_DATA_FILE))
    df = spark_engine.to_pandas(spark_df)
    return df


def show():
    """Display visualizations page"""
    st.title("📊 Interactive Visualizations")
    st.markdown("Professional charts and statistical visualizations")
    st.markdown("---")
    
    # Load data
    with st.spinner("Loading data..."):
        df = load_viz_data()
        analytics = AnalyticsEngine(df)
    
    # Visualization type selector
    viz_type = st.selectbox(
        "Select Visualization Type",
        [
            "Correlation Analysis",
            "Distribution Analysis",
            "Box Plots",
            "Scatter Plots",
            "Comparative Analysis"
        ]
    )
    
    st.markdown("---")
    
    if viz_type == "Correlation Analysis":
        show_correlation_viz(df, analytics)
    elif viz_type == "Distribution Analysis":
        show_distribution_viz(df)
    elif viz_type == "Box Plots":
        show_box_plots(df)
    elif viz_type == "Scatter Plots":
        show_scatter_plots(df)
    elif viz_type == "Comparative Analysis":
        show_comparative_viz(df)


def show_correlation_viz(df, analytics):
    """Show correlation visualizations"""
    st.subheader("🔗 Correlation Analysis")
    st.write("Explore relationships between numerical features")
    
    # Calculate correlation
    corr_matrix = analytics.correlation_analysis()
    
    # Display heatmap
    fig = create_correlation_heatmap(corr_matrix, "Feature Correlation Matrix")
    st.pyplot(fig)
    
    st.markdown("---")
    
    # Correlation insights
    st.write("**Key Correlations:**")
    
    # Find strong correlations
    strong_corr = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_val = corr_matrix.iloc[i, j]
            if abs(corr_val) > 0.3:  # Threshold for "strong"
                strong_corr.append({
                    'Feature 1': corr_matrix.columns[i],
                    'Feature 2': corr_matrix.columns[j],
                    'Correlation': corr_val
                })
    
    if strong_corr:
        corr_df = pd.DataFrame(strong_corr).sort_values('Correlation', ascending=False)
        st.dataframe(corr_df, use_container_width=True, hide_index=True)
    else:
        st.info("No strong correlations found (threshold: 0.3)")


def show_distribution_viz(df):
    """Show distribution visualizations"""
    st.subheader("📈 Distribution Analysis")
    st.write("Analyze the distribution of numerical features")
    
    # Feature selector
    feature = st.selectbox(
        "Select Feature",
        ['Temparature', 'Humidity', 'Moisture', 'Nitrogen', 'Potassium', 'Phosphorous']
    )
    
    # Create distribution plot
    fig = create_distribution_plot(
        df[feature],
        f"Distribution of {feature}",
        feature
    )
    st.pyplot(fig)
    
    st.markdown("---")
    
    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Mean", f"{df[feature].mean():.2f}")
    
    with col2:
        st.metric("Median", f"{df[feature].median():.2f}")
    
    with col3:
        st.metric("Std Dev", f"{df[feature].std():.2f}")
    
    with col4:
        st.metric("Range", f"{df[feature].max() - df[feature].min():.2f}")


def show_box_plots(df):
    """Show box plot visualizations"""
    st.subheader("📦 Box Plot Analysis")
    st.write("Compare distributions across categories")
    
    col1, col2 = st.columns(2)
    
    with col1:
        feature = st.selectbox(
            "Select Numerical Feature",
            ['Temparature', 'Humidity', 'Moisture', 'Nitrogen', 'Potassium', 'Phosphorous']
        )
    
    with col2:
        group_by = st.selectbox(
            "Group By",
            ['Crop Type', 'Soil Type', 'Fertilizer Name']
        )
    
    # Create box plot
    fig = create_box_plot(
        df,
        feature,
        group_by,
        f"{feature} Distribution by {group_by}"
    )
    st.pyplot(fig)
    
    st.markdown("---")
    
    # Summary statistics by group
    st.write(f"**{feature} Statistics by {group_by}:**")
    summary = df.groupby(group_by)[feature].describe()
    st.dataframe(summary, use_container_width=True)


def show_scatter_plots(df):
    """Show scatter plot visualizations"""
    st.subheader("🎯 Scatter Plot Analysis")
    st.write("Explore relationships between two features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        x_feature = st.selectbox(
            "X-Axis Feature",
            ['Temparature', 'Humidity', 'Moisture', 'Nitrogen', 'Potassium', 'Phosphorous'],
            index=0
        )
    
    with col2:
        y_feature = st.selectbox(
            "Y-Axis Feature",
            ['Temparature', 'Humidity', 'Moisture', 'Nitrogen', 'Potassium', 'Phosphorous'],
            index=1
        )
    
    with col3:
        color_by = st.selectbox(
            "Color By (Optional)",
            ['None', 'Crop Type', 'Soil Type', 'Fertilizer Name']
        )
    
    # Sample data for performance (use 5000 points)
    sample_df = df.sample(n=min(5000, len(df)), random_state=42)
    
    # Create scatter plot
    hue = None if color_by == 'None' else color_by
    fig = create_scatter_plot(
        sample_df,
        x_feature,
        y_feature,
        f"{y_feature} vs {x_feature}",
        hue=hue
    )
    st.pyplot(fig)
    
    st.info(f"Showing {len(sample_df)} sample points for performance")


def show_comparative_viz(df):
    """Show comparative visualizations"""
    st.subheader("⚖️ Comparative Analysis")
    st.write("Compare metrics across different categories")
    
    # Select comparison type
    comparison = st.selectbox(
        "Select Comparison",
        [
            "Nutrients by Crop",
            "Nutrients by Soil",
            "Environmental Factors by Crop",
            "Environmental Factors by Soil"
        ]
    )
    
    if comparison == "Nutrients by Crop":
        # Group by crop and calculate average nutrients
        nutrient_data = df.groupby('Crop Type')[['Nitrogen', 'Potassium', 'Phosphorous']].mean()
        fig = create_grouped_bar_chart(
            nutrient_data,
            "Average Nutrients by Crop Type",
            "Crop Type",
            "Average Level"
        )
        st.pyplot(fig)
    
    elif comparison == "Nutrients by Soil":
        # Group by soil and calculate average nutrients
        nutrient_data = df.groupby('Soil Type')[['Nitrogen', 'Potassium', 'Phosphorous']].mean()
        fig = create_grouped_bar_chart(
            nutrient_data,
            "Average Nutrients by Soil Type",
            "Soil Type",
            "Average Level"
        )
        st.pyplot(fig)
    
    elif comparison == "Environmental Factors by Crop":
        # Group by crop and calculate average environmental factors
        env_data = df.groupby('Crop Type')[['Temparature', 'Humidity', 'Moisture']].mean()
        fig = create_grouped_bar_chart(
            env_data,
            "Average Environmental Factors by Crop Type",
            "Crop Type",
            "Average Value"
        )
        st.pyplot(fig)
    
    elif comparison == "Environmental Factors by Soil":
        # Group by soil and calculate average environmental factors
        env_data = df.groupby('Soil Type')[['Temparature', 'Humidity', 'Moisture']].mean()
        fig = create_grouped_bar_chart(
            env_data,
            "Average Environmental Factors by Soil Type",
            "Soil Type",
            "Average Value"
        )
        st.pyplot(fig)
    
    st.markdown("---")
    
    # Show data table
    st.write("**Detailed Data:**")
    if "Nutrients" in comparison:
        if "Crop" in comparison:
            data = df.groupby('Crop Type')[['Nitrogen', 'Potassium', 'Phosphorous']].mean()
        else:
            data = df.groupby('Soil Type')[['Nitrogen', 'Potassium', 'Phosphorous']].mean()
    else:
        if "Crop" in comparison:
            data = df.groupby('Crop Type')[['Temparature', 'Humidity', 'Moisture']].mean()
        else:
            data = df.groupby('Soil Type')[['Temparature', 'Humidity', 'Moisture']].mean()
    
    st.dataframe(data, use_container_width=True)

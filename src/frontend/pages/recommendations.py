"""
Recommendations page - Interactive fertilizer recommendation system
"""
import streamlit as st
import pandas as pd
import sys
sys.path.append('/home/faaris/projects/BDA/fert-predict')
from src.backend.spark_engine import spark_engine
from src.backend.recommendation_engine import RecommendationEngine
from src.utils.helpers import create_download_filename
from config.settings import MAIN_DATA_FILE, CROP_TYPES, SOIL_TYPES


@st.cache_resource
def load_recommendation_engine():
    """Load and cache recommendation engine"""
    spark_df = spark_engine.load_data(str(MAIN_DATA_FILE))
    df = spark_engine.to_pandas(spark_df)
    return RecommendationEngine(df)


def show():
    """Display recommendations page"""
    st.title("🎯 Fertilizer Recommendation System")
    st.markdown("Get intelligent fertilizer recommendations based on your conditions")
    st.markdown("---")
    
    # Load recommendation engine
    with st.spinner("Loading recommendation engine..."):
        rec_engine = load_recommendation_engine()
    
    # Recommendation mode
    mode = st.radio(
        "Select Mode",
        ["Single Recommendation", "Batch Recommendations"],
        horizontal=True
    )
    
    st.markdown("---")
    
    if mode == "Single Recommendation":
        show_single_recommendation(rec_engine)
    else:
        show_batch_recommendations(rec_engine)


def show_single_recommendation(rec_engine):
    """Show single recommendation interface"""
    st.subheader("🌾 Get Fertilizer Recommendation")
    
    # Input form
    with st.form("recommendation_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Environmental Conditions:**")
            temperature = st.slider("Temperature (°C)", 25, 40, 30)
            humidity = st.slider("Humidity (%)", 50, 75, 60)
            moisture = st.slider("Moisture (%)", 25, 65, 40)
        
        with col2:
            st.write("**Crop & Soil Information:**")
            crop_type = st.selectbox("Crop Type", sorted(CROP_TYPES))
            soil_type = st.selectbox("Soil Type", sorted(SOIL_TYPES))
            
            st.write("**Nutrient Levels (Optional):**")
            include_nutrients = st.checkbox("Include current nutrient levels")
        
        if include_nutrients:
            col3, col4, col5 = st.columns(3)
            with col3:
                nitrogen = st.number_input("Nitrogen", 0, 50, 20)
            with col4:
                potassium = st.number_input("Potassium", 0, 50, 10)
            with col5:
                phosphorous = st.number_input("Phosphorous", 0, 50, 15)
        else:
            nitrogen = None
            potassium = None
            phosphorous = None
        
        submitted = st.form_submit_button("🔍 Get Recommendation", use_container_width=True)
    
    if submitted:
        # Get recommendation
        with st.spinner("Analyzing conditions..."):
            recommendation = rec_engine.recommend(
                temperature=temperature,
                humidity=humidity,
                moisture=moisture,
                soil_type=soil_type,
                crop_type=crop_type,
                nitrogen=nitrogen,
                potassium=potassium,
                phosphorous=phosphorous
            )
        
        # Display results
        st.markdown("---")
        st.subheader("📊 Recommendation Results")
        
        # Primary recommendation
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.success(f"### 🎯 Recommended Fertilizer: **{recommendation['primary_recommendation']}**")
            st.write(recommendation['explanation'])
        
        with col2:
            # Confidence gauge
            confidence = recommendation['confidence_score']
            confidence_pct = confidence * 100
            
            if confidence >= 0.8:
                color = "🟢"
                status = "High Confidence"
            elif confidence >= 0.6:
                color = "🟡"
                status = "Medium Confidence"
            else:
                color = "🔴"
                status = "Low Confidence"
            
            st.metric("Confidence Score", f"{confidence_pct:.0f}%", delta=status)
            st.write(f"{color} {status}")
        
        st.markdown("---")
        
        # Alternative recommendations
        if recommendation['alternatives']:
            st.write("### 🔄 Alternative Recommendations")
            col1, col2 = st.columns(2)
            
            for i, alt in enumerate(recommendation['alternatives'][:2], 1):
                with col1 if i == 1 else col2:
                    st.info(f"**Alternative {i}:** {alt}")
        
        # Nutrient analysis
        if recommendation['nutrient_analysis']:
            st.markdown("---")
            st.write("### 💊 Nutrient Analysis")
            
            nutrient_data = recommendation['nutrient_analysis']
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Expected Nitrogen",
                    f"{nutrient_data.get('expected_nitrogen', 'N/A')}"
                )
                if 'nitrogen_status' in nutrient_data:
                    status = nutrient_data['nitrogen_status']
                    if status == 'adequate':
                        st.success("✅ Adequate")
                    else:
                        st.warning("⚠️ Deficient")
            
            with col2:
                st.metric(
                    "Expected Potassium",
                    f"{nutrient_data.get('expected_potassium', 'N/A')}"
                )
                if 'potassium_status' in nutrient_data:
                    status = nutrient_data['potassium_status']
                    if status == 'adequate':
                        st.success("✅ Adequate")
                    else:
                        st.warning("⚠️ Deficient")
            
            with col3:
                st.metric(
                    "Expected Phosphorous",
                    f"{nutrient_data.get('expected_phosphorous', 'N/A')}"
                )
                if 'phosphorous_status' in nutrient_data:
                    status = nutrient_data['phosphorous_status']
                    if status == 'adequate':
                        st.success("✅ Adequate")
                    else:
                        st.warning("⚠️ Deficient")


def show_batch_recommendations(rec_engine):
    """Show batch recommendation interface"""
    st.subheader("📦 Batch Recommendations")
    st.write("Upload a CSV file with multiple conditions to get recommendations for all")
    
    # Sample template
    st.write("### 📋 CSV Template")
    st.info("""
    Your CSV file should contain the following columns:
    - **Temparature** (or Temperature): Temperature in Celsius
    - **Humidity**: Humidity percentage
    - **Moisture**: Moisture percentage
    - **Soil Type**: Type of soil (Red, Black, Sandy, Loamy, Clayey)
    - **Crop Type**: Type of crop
    - **Nitrogen** (optional): Current nitrogen level
    - **Potassium** (optional): Current potassium level
    - **Phosphorous** (optional): Current phosphorous level
    """)
    
    # Download sample template
    sample_data = pd.DataFrame({
        'Temparature': [30, 32, 28],
        'Humidity': [60, 55, 65],
        'Moisture': [40, 45, 38],
        'Soil Type': ['Loamy', 'Red', 'Black'],
        'Crop Type': ['Wheat', 'Cotton', 'Paddy'],
        'Nitrogen': [20, 25, 18],
        'Potassium': [10, 12, 8],
        'Phosphorous': [15, 18, 12]
    })
    
    csv_template = sample_data.to_csv(index=False)
    st.download_button(
        label="📥 Download Sample Template",
        data=csv_template,
        file_name="recommendation_template.csv",
        mime="text/csv"
    )
    
    st.markdown("---")
    
    # File upload
    uploaded_file = st.file_uploader("Upload CSV File", type=['csv'])
    
    if uploaded_file is not None:
        try:
            # Read uploaded file
            input_df = pd.read_csv(uploaded_file)
            
            st.write("### 📊 Uploaded Data Preview")
            st.dataframe(input_df.head(10), use_container_width=True)
            
            st.write(f"**Total Records:** {len(input_df)}")
            
            # Generate recommendations
            if st.button("🚀 Generate Recommendations", use_container_width=True):
                with st.spinner(f"Generating recommendations for {len(input_df)} records..."):
                    results_df = rec_engine.batch_recommend(input_df)
                
                st.success(f"✅ Generated {len(results_df)} recommendations!")
                
                # Combine input and results
                combined_df = pd.concat([input_df.reset_index(drop=True), results_df], axis=1)
                
                st.write("### 📋 Recommendation Results")
                st.dataframe(combined_df, use_container_width=True)
                
                # Download results
                csv_results = combined_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Results (CSV)",
                    data=csv_results,
                    file_name=create_download_filename("batch_recommendations"),
                    mime="text/csv"
                )
                
                # Summary statistics
                st.markdown("---")
                st.write("### 📊 Recommendation Summary")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Recommended Fertilizers:**")
                    fert_counts = results_df['Recommended_Fertilizer'].value_counts()
                    for fert, count in fert_counts.items():
                        pct = (count / len(results_df)) * 100
                        st.write(f"- {fert}: {count} ({pct:.1f}%)")
                
                with col2:
                    st.write("**Confidence Distribution:**")
                    avg_confidence = results_df['Confidence'].mean()
                    high_conf = len(results_df[results_df['Confidence'] >= 0.8])
                    med_conf = len(results_df[(results_df['Confidence'] >= 0.6) & (results_df['Confidence'] < 0.8)])
                    low_conf = len(results_df[results_df['Confidence'] < 0.6])
                    
                    st.metric("Average Confidence", f"{avg_confidence:.2f}")
                    st.write(f"- High (≥0.8): {high_conf}")
                    st.write(f"- Medium (0.6-0.8): {med_conf}")
                    st.write(f"- Low (<0.6): {low_conf}")
        
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            st.info("Please ensure your CSV file matches the required format.")

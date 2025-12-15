"""
Main Streamlit Application - Fertilizer Prediction & Analytics
"""
import streamlit as st
import sys
sys.path.append('/home/faaris/projects/BDA/fert-predict')
from config.settings import PAGE_CONFIG, APP_TITLE

# Page configuration
st.set_page_config(**PAGE_CONFIG)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
""", unsafe_allow_html=True)

# Main header
st.markdown(f'<div class="main-header">{APP_TITLE}</div>', unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("📊 Navigation")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Select Page",
    ["🏠 Dashboard", "📈 Analysis", "📊 Visualizations", "📄 Reports", "🎯 Recommendations"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.info("""
**About This Application**

This application provides comprehensive fertilizer prediction and analytics using:
- **PySpark** for big data processing
- **Advanced Analytics** for insights
- **ML-based Recommendations**
- **Interactive Visualizations**

Analyze 100K+ agricultural records to make data-driven decisions.
""")

# Route to appropriate page
if page == "🏠 Dashboard":
    from src.frontend.pages import dashboard
    dashboard.show()
elif page == "📈 Analysis":
    from src.frontend.pages import analysis
    analysis.show()
elif page == "📊 Visualizations":
    from src.frontend.pages import visualizations
    visualizations.show()
elif page == "📄 Reports":
    from src.frontend.pages import reports
    reports.show()
elif page == "🎯 Recommendations":
    from src.frontend.pages import recommendations
    recommendations.show()

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Fertilizer Prediction System v1.0**")
st.sidebar.markdown("*Powered by PySpark & Streamlit*")

# Fertilizer Prediction & Analytics Application

A comprehensive fertilizer prediction and analytics application built with **Streamlit**, **PySpark**, and advanced machine learning techniques. This application provides intelligent fertilizer recommendations, detailed analytics, and interactive visualizations for agricultural decision-making.

## 🌟 Features

### 📊 Interactive Dashboard
- Real-time key performance indicators (KPIs)
- Fertilizer and soil type distribution charts
- Top crop statistics
- Environmental condition metrics
- Quick insights and recommendations

### 📈 Multi-Dimensional Analysis
- **By Crop Type**: Analyze fertilizer usage, soil preferences, and nutrient requirements
- **By Soil Type**: Discover suitable crops and optimal fertilizers
- **By Fertilizer**: Understand usage patterns and environmental conditions
- **Nutrient Analysis**: Comprehensive nutrient distribution across crops and soils
- **Environmental Analysis**: Temperature, humidity, and moisture patterns

### 📊 Professional Visualizations
- Correlation heatmaps for feature relationships
- Distribution plots with KDE curves
- Box plots for categorical comparisons
- Scatter plots with color coding
- Grouped bar charts for comparative analysis

### 📄 Executive Reports
- Automated executive summaries with key insights
- Data quality assessment reports
- Crop performance analysis
- Fertilizer usage statistics
- Environmental condition reports
- Downloadable CSV reports

### 🎯 Intelligent Recommendations
- **Single Recommendation Mode**: Get instant fertilizer recommendations
- **Batch Processing**: Upload CSV files for bulk recommendations
- Confidence scoring for each recommendation
- Alternative fertilizer suggestions
- Nutrient deficiency analysis
- Explanation for each recommendation

## 🚀 Technology Stack

### Backend
- **PySpark 3.5.0**: Distributed data processing for 100K+ records
- **Pandas 2.1.4**: Data manipulation and analysis
- **NumPy 1.26.2**: Numerical computations
- **Scikit-learn 1.3.2**: Machine learning utilities

### Frontend
- **Streamlit 1.29.0**: Interactive web interface
- **Matplotlib 3.8.2**: Static visualizations
- **Seaborn 0.13.0**: Statistical data visualization
- **Plotly 5.18.0**: Interactive charts

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Java 8 or higher (for PySpark)

### Setup

1. **Clone or navigate to the project directory:**
```bash
cd /home/faaris/projects/BDA/fert-predict
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## 🎮 Usage

### Running the Application

Start the Streamlit application:
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Navigation

The application has 5 main pages accessible from the sidebar:

1. **🏠 Dashboard**: Overview and key metrics
2. **📈 Analysis**: Detailed multi-dimensional analysis
3. **📊 Visualizations**: Interactive charts and graphs
4. **📄 Reports**: Executive summaries and insights
5. **🎯 Recommendations**: Fertilizer recommendation system

### Getting Recommendations

#### Single Recommendation:
1. Navigate to the **Recommendations** page
2. Select "Single Recommendation" mode
3. Enter environmental conditions (temperature, humidity, moisture)
4. Select crop and soil type
5. Optionally add current nutrient levels
6. Click "Get Recommendation"

#### Batch Recommendations:
1. Navigate to the **Recommendations** page
2. Select "Batch Recommendations" mode
3. Download the sample CSV template
4. Fill in your data
5. Upload the CSV file
6. Click "Generate Recommendations"
7. Download the results

## 📊 Dataset

The application uses the **Fertilizer Prediction** dataset with 100,000+ records containing:

- **Environmental Factors**: Temperature, Humidity, Moisture
- **Soil Information**: Soil Type (Red, Black, Sandy, Loamy, Clayey)
- **Crop Information**: 11 crop types (Wheat, Cotton, Paddy, Maize, etc.)
- **Nutrient Levels**: Nitrogen, Potassium, Phosphorous
- **Target**: Fertilizer Name (7 types: Urea, DAP, 14-35-14, 28-28, 20-20, 17-17-17, 10-26-26)

## 🏗️ Project Structure

```
fert-predict/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── .streamlit/
│   └── config.toml                # Streamlit configuration
├── config/
│   └── settings.py                # Application settings
├── data/
│   └── Fertilizer Prediction.csv  # Dataset
├── src/
│   ├── backend/
│   │   ├── spark_engine.py        # PySpark data processing
│   │   ├── data_processor.py      # Data preprocessing
│   │   ├── analytics_engine.py    # Analytics and insights
│   │   └── recommendation_engine.py # Recommendation system
│   ├── frontend/
│   │   ├── pages/
│   │   │   ├── dashboard.py       # Dashboard page
│   │   │   ├── analysis.py        # Analysis page
│   │   │   ├── visualizations.py  # Visualizations page
│   │   │   ├── reports.py         # Reports page
│   │   │   └── recommendations.py # Recommendations page
│   │   └── components/
│   │       └── charts.py          # Reusable chart components
│   └── utils/
│       └── helpers.py             # Utility functions
└── tests/                         # Test files (future)
```

## 🎨 Features Highlight

### Big Data Processing
- Handles 1M+ row datasets efficiently using PySpark
- Distributed computing for fast analytics
- Optimized caching strategies

### Advanced Analytics
- Multi-dimensional analysis across crops, soils, and fertilizers
- Correlation analysis between features
- Statistical insights and pattern detection
- Automated insight generation

### Intelligent Recommendations
- Rule-based recommendation using historical patterns
- Similarity-based matching for edge cases
- Confidence scoring for transparency
- Nutrient deficiency detection
- Batch processing for multiple recommendations

### Professional Visualizations
- Publication-quality charts
- Consistent color schemes
- Interactive elements
- Export functionality

## 🔧 Configuration

Edit `config/settings.py` to customize:
- Spark configuration parameters
- Color schemes for visualizations
- Data file paths
- Feature definitions

Edit `.streamlit/config.toml` to customize:
- Theme colors
- Server settings
- Browser behavior

## 📝 License

This project is for educational and research purposes.

## 👥 Contributors

Developed as part of Big Data Analytics coursework.

## 🙏 Acknowledgments

- Dataset source: Fertilizer Prediction Dataset
- Built with Streamlit, PySpark, and Python ecosystem

## 📧 Support

For issues or questions, please create an issue in the project repository.

---

**Made with ❤️ using PySpark & Streamlit**

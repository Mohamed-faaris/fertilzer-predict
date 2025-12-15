# Deployment Guide - Fertilizer Prediction Application

## Prerequisites

Before deploying the application, ensure you have the following installed:

### System Requirements
- **Python 3.8+** (Python 3.9 or 3.10 recommended)
- **Java 8 or 11** (required for PySpark)
- **4GB RAM minimum** (8GB recommended for large datasets)

### Check Java Installation
```bash
java -version
```

If Java is not installed:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install openjdk-11-jdk

# macOS
brew install openjdk@11

# Windows
# Download from https://adoptium.net/
```

## Installation Steps

### 1. Set Up Virtual Environment

It's highly recommended to use a virtual environment:

```bash
# Navigate to project directory
cd /home/faaris/projects/BDA/fert-predict

# Install python3-venv if not available (Ubuntu/Debian)
sudo apt install python3-venv

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

This will install:
- pyspark==3.5.0
- streamlit==1.29.0
- pandas==2.1.4
- numpy==1.26.2
- matplotlib==3.8.2
- seaborn==0.13.0
- plotly==5.18.0
- scikit-learn==1.3.2
- openpyxl==3.1.2

### 3. Verify Installation

```bash
# Check PySpark
python -c "import pyspark; print('PySpark:', pyspark.__version__)"

# Check Streamlit
streamlit --version

# Check other packages
python -c "import pandas, numpy, matplotlib, seaborn; print('All packages OK')"
```

## Running the Application

### Start the Application

```bash
# Make sure you're in the project directory
cd /home/faaris/projects/BDA/fert-predict

# Activate virtual environment (if not already activated)
source venv/bin/activate

# Run the Streamlit app
streamlit run app.py
```

The application will start and automatically open in your default browser at:
```
http://localhost:8501
```

### Alternative: Specify Port

```bash
streamlit run app.py --server.port 8080
```

### Run in Headless Mode (Server Deployment)

```bash
streamlit run app.py --server.headless true
```

## Configuration

### Streamlit Configuration

Edit `.streamlit/config.toml` to customize:

```toml
[theme]
primaryColor = "#4CAF50"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F5F5F5"
textColor = "#262730"

[server]
port = 8501
enableCORS = false
```

### Application Settings

Edit `config/settings.py` to customize:
- Spark configuration (memory, partitions)
- Data file paths
- Color schemes
- Feature definitions

## Troubleshooting

### Issue: PySpark Not Found
```bash
# Reinstall PySpark
pip install --force-reinstall pyspark==3.5.0
```

### Issue: Java Not Found
```bash
# Set JAVA_HOME environment variable
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
```

### Issue: Memory Errors with Large Datasets
Edit `config/settings.py` and increase Spark memory:
```python
SPARK_CONFIG = {
    "spark.driver.memory": "8g",  # Increase from 4g
    "spark.executor.memory": "8g",
}
```

### Issue: Port Already in Use
```bash
# Use a different port
streamlit run app.py --server.port 8502
```

### Issue: Matplotlib Backend Errors
```bash
# Install additional dependencies
pip install python-tk
```

## Performance Optimization

### For Large Datasets (1M+ rows)

1. **Increase Spark Partitions:**
```python
# In config/settings.py
"spark.sql.shuffle.partitions": "16",  # Increase from 8
```

2. **Enable Caching:**
The application already uses `@st.cache_data` decorators, but you can clear cache if needed:
```
Press 'C' in the Streamlit app, or
Click the hamburger menu → Clear cache
```

3. **Use Sampling for Visualizations:**
The scatter plot page already samples 5000 points for performance.

## Production Deployment

### Using Docker (Recommended)

Create a `Dockerfile`:
```dockerfile
FROM python:3.10-slim

# Install Java
RUN apt-get update && apt-get install -y openjdk-11-jdk

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8501

# Run application
CMD ["streamlit", "run", "app.py", "--server.headless", "true"]
```

Build and run:
```bash
docker build -t fert-predict .
docker run -p 8501:8501 fert-predict
```

### Using Cloud Platforms

#### Streamlit Cloud
1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Connect repository
4. Deploy

#### Heroku
```bash
# Create Procfile
echo "web: streamlit run app.py --server.port $PORT" > Procfile

# Deploy
heroku create fert-predict-app
git push heroku main
```

#### AWS EC2
1. Launch EC2 instance (t2.medium or larger)
2. Install dependencies
3. Run with screen or tmux:
```bash
screen -S streamlit
streamlit run app.py
# Detach with Ctrl+A, D
```

## Security Considerations

### For Production:

1. **Enable Authentication:**
```bash
# Install streamlit-authenticator
pip install streamlit-authenticator
```

2. **Use HTTPS:**
Configure reverse proxy (nginx/Apache) with SSL certificate

3. **Restrict Access:**
```toml
# In .streamlit/config.toml
[server]
enableCORS = false
enableXsrfProtection = true
```

## Monitoring

### Check Application Logs
```bash
# Streamlit logs are in terminal
# Redirect to file:
streamlit run app.py > app.log 2>&1
```

### Monitor Resource Usage
```bash
# CPU and memory
htop

# Spark UI (when running)
# Access at http://localhost:4040
```

## Backup and Maintenance

### Backup Data
```bash
# Backup dataset
cp -r data/ data_backup_$(date +%Y%m%d)/
```

### Update Dependencies
```bash
# Update all packages
pip install --upgrade -r requirements.txt

# Or update specific package
pip install --upgrade streamlit
```

## Support

For issues:
1. Check the troubleshooting section above
2. Review Streamlit documentation: https://docs.streamlit.io
3. Check PySpark documentation: https://spark.apache.org/docs/latest/

---

**Ready to Deploy!** Follow these steps and your application will be up and running.

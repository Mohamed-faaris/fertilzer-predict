"""
PySpark Engine for distributed data processing
Fallback to Pandas if PySpark is not available
"""
try:
    from pyspark.sql import SparkSession
    from pyspark.sql import DataFrame as SparkDataFrame
    from pyspark.sql.functions import col, count, avg, sum as spark_sum, min as spark_min, max as spark_max
    PYSPARK_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    PYSPARK_AVAILABLE = False
    print("⚠️  PySpark not available, using Pandas-only mode")

import pandas as pd
import sys
sys.path.append('/home/faaris/projects/BDA/fert-predict')
from config.settings import SPARK_CONFIG, MAIN_DATA_FILE
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SparkEngine:
    """Singleton Spark Engine for data processing (with Pandas fallback)"""
    
    _instance = None
    _spark = None
    _use_pandas = not PYSPARK_AVAILABLE
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SparkEngine, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize Spark session with optimized configuration"""
        if not self._use_pandas and self._spark is None:
            self._initialize_spark()
        elif self._use_pandas:
            logger.info("Using Pandas-only mode (PySpark not available)")
    
    def _initialize_spark(self):
        """Create and configure Spark session"""
        if self._use_pandas:
            return
            
        try:
            builder = SparkSession.builder
            
            # Apply configuration
            for key, value in SPARK_CONFIG.items():
                builder = builder.config(key, value)
            
            self._spark = builder.getOrCreate()
            self._spark.sparkContext.setLogLevel("WARN")
            logger.info("Spark session initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Spark: {e}")
            logger.info("Falling back to Pandas-only mode")
            self._use_pandas = True
    
    @property
    def spark(self):
        """Get Spark session"""
        return self._spark
    
    def load_data(self, file_path: str = None, cache: bool = True):
        """
        Load data from CSV file
        
        Args:
            file_path: Path to CSV file (defaults to main data file)
            cache: Whether to cache the DataFrame
            
        Returns:
            Pandas DataFrame (always returns Pandas for compatibility)
        """
        if file_path is None:
            file_path = str(MAIN_DATA_FILE)
        
        try:
            logger.info(f"Loading data from {file_path}")
            
            if self._use_pandas:
                # Use Pandas directly
                df = pd.read_csv(file_path)
                logger.info(f"Loaded {len(df)} records using Pandas")
                return df
            else:
                # Use PySpark and convert to Pandas
                spark_df = self._spark.read.csv(
                    file_path,
                    header=True,
                    inferSchema=True
                )
                
                if cache:
                    spark_df = spark_df.cache()
                
                df = spark_df.toPandas()
                logger.info(f"Loaded {len(df)} records using PySpark")
                return df
            
        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            # Fallback to Pandas
            logger.info("Attempting to load with Pandas...")
            df = pd.read_csv(file_path)
            logger.info(f"Loaded {len(df)} records using Pandas (fallback)")
            return df
    
    def get_summary_stats(self, df: pd.DataFrame, columns: list = None) -> dict:
        """
        Get summary statistics for specified columns
        
        Args:
            df: Pandas DataFrame
            columns: List of columns (None for all numeric columns)
            
        Returns:
            Dictionary of statistics
        """
        if columns is None:
            columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        
        stats = {}
        for column in columns:
            if column in df.columns:
                stats[column] = {
                    'min': float(df[column].min()),
                    'max': float(df[column].max()),
                    'mean': float(df[column].mean()),
                    'count': int(df[column].count())
                }
        
        return stats
    
    def group_and_aggregate(self, df: pd.DataFrame, group_by: str, agg_column: str = None) -> pd.DataFrame:
        """
        Group by column and aggregate
        
        Args:
            df: Pandas DataFrame
            group_by: Column to group by
            agg_column: Column to aggregate (None for count only)
            
        Returns:
            Aggregated DataFrame
        """
        if agg_column:
            return df.groupby(group_by).agg(
                count=(group_by, 'count'),
                **{f'avg_{agg_column}': (agg_column, 'mean')}
            ).reset_index()
        else:
            return df.groupby(group_by).size().reset_index(name='count')
    
    def filter_data(self, df: pd.DataFrame, conditions: dict) -> pd.DataFrame:
        """
        Filter DataFrame based on conditions
        
        Args:
            df: Pandas DataFrame
            conditions: Dictionary of column: value pairs
            
        Returns:
            Filtered DataFrame
        """
        filtered_df = df.copy()
        for column, value in conditions.items():
            if isinstance(value, list):
                filtered_df = filtered_df[filtered_df[column].isin(value)]
            else:
                filtered_df = filtered_df[filtered_df[column] == value]
        
        return filtered_df
    
    def to_pandas(self, df: pd.DataFrame, limit: int = None):
        """
        Convert to Pandas (already Pandas, so just return or limit)
        
        Args:
            df: Pandas DataFrame
            limit: Maximum number of rows (None for all)
            
        Returns:
            Pandas DataFrame
        """
        if limit:
            return df.head(limit)
        return df
    
    def stop(self):
        """Stop Spark session"""
        if self._spark and not self._use_pandas:
            self._spark.stop()
            logger.info("Spark session stopped")


# Global instance
spark_engine = SparkEngine()

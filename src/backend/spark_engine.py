"""
PySpark Engine for distributed data processing
"""
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, count, avg, sum as spark_sum, min as spark_min, max as spark_max
import sys
sys.path.append('/home/faaris/projects/BDA/fert-predict')
from config.settings import SPARK_CONFIG, MAIN_DATA_FILE
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SparkEngine:
    """Singleton Spark Engine for data processing"""
    
    _instance = None
    _spark = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SparkEngine, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize Spark session with optimized configuration"""
        if self._spark is None:
            self._initialize_spark()
    
    def _initialize_spark(self):
        """Create and configure Spark session"""
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
            raise
    
    @property
    def spark(self) -> SparkSession:
        """Get Spark session"""
        return self._spark
    
    def load_data(self, file_path: str = None, cache: bool = True) -> DataFrame:
        """
        Load data from CSV file
        
        Args:
            file_path: Path to CSV file (defaults to main data file)
            cache: Whether to cache the DataFrame
            
        Returns:
            Spark DataFrame
        """
        if file_path is None:
            file_path = str(MAIN_DATA_FILE)
        
        try:
            logger.info(f"Loading data from {file_path}")
            df = self._spark.read.csv(
                file_path,
                header=True,
                inferSchema=True
            )
            
            if cache:
                df = df.cache()
            
            logger.info(f"Loaded {df.count()} records")
            return df
            
        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            raise
    
    def get_summary_stats(self, df: DataFrame, columns: list = None) -> dict:
        """
        Get summary statistics for specified columns
        
        Args:
            df: Spark DataFrame
            columns: List of columns (None for all numeric columns)
            
        Returns:
            Dictionary of statistics
        """
        if columns is None:
            # Get all numeric columns
            columns = [field.name for field in df.schema.fields 
                      if field.dataType.typeName() in ['integer', 'double', 'float', 'long']]
        
        stats = {}
        for column in columns:
            col_stats = df.select(
                spark_min(col(column)).alias('min'),
                spark_max(col(column)).alias('max'),
                avg(col(column)).alias('mean'),
                count(col(column)).alias('count')
            ).collect()[0]
            
            stats[column] = {
                'min': col_stats['min'],
                'max': col_stats['max'],
                'mean': col_stats['mean'],
                'count': col_stats['count']
            }
        
        return stats
    
    def group_and_aggregate(self, df: DataFrame, group_by: str, agg_column: str = None) -> DataFrame:
        """
        Group by column and aggregate
        
        Args:
            df: Spark DataFrame
            group_by: Column to group by
            agg_column: Column to aggregate (None for count only)
            
        Returns:
            Aggregated DataFrame
        """
        if agg_column:
            return df.groupBy(group_by).agg(
                count("*").alias("count"),
                avg(col(agg_column)).alias(f"avg_{agg_column}")
            )
        else:
            return df.groupBy(group_by).agg(count("*").alias("count"))
    
    def filter_data(self, df: DataFrame, conditions: dict) -> DataFrame:
        """
        Filter DataFrame based on conditions
        
        Args:
            df: Spark DataFrame
            conditions: Dictionary of column: value pairs
            
        Returns:
            Filtered DataFrame
        """
        filtered_df = df
        for column, value in conditions.items():
            if isinstance(value, list):
                filtered_df = filtered_df.filter(col(column).isin(value))
            else:
                filtered_df = filtered_df.filter(col(column) == value)
        
        return filtered_df
    
    def to_pandas(self, df: DataFrame, limit: int = None):
        """
        Convert Spark DataFrame to Pandas
        
        Args:
            df: Spark DataFrame
            limit: Maximum number of rows (None for all)
            
        Returns:
            Pandas DataFrame
        """
        if limit:
            df = df.limit(limit)
        
        return df.toPandas()
    
    def stop(self):
        """Stop Spark session"""
        if self._spark:
            self._spark.stop()
            logger.info("Spark session stopped")


# Global instance
spark_engine = SparkEngine()

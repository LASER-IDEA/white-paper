"""
Dataset Loader for LAEV Experiments
Loads real flight data and prepares it for NL4DV and our system
"""

import pandas as pd
import json
from typing import Dict, Any, Optional
from pathlib import Path


class LAEVDataset:
    """
    Low Altitude Economy Visualization Dataset
    
    Real flight data from Shenzhen low-altitude operations.
    500 records, 18 attributes covering temporal, spatial, 
    categorical, and numerical dimensions.
    """
    
    DATA_PATH = Path(__file__).parent / "sample_flight_data.csv"
    
    # Domain-specific metadata for semantic understanding
    DOMAIN_METADATA = {
        "name": "Shenzhen Low Altitude Flight Operations",
        "description": "Real flight records from Shenzhen low-altitude economy operations in 2023",
        "source": "Low Altitude Economy White Paper",
        "record_count": 500,
        "time_range": "2023-01-01 to 2023-12-31",
        "spatial_coverage": "Shenzhen districts",
        
        "attribute_semantics": {
            "date": {
                "type": "temporal",
                "description": "Flight operation date",
                "granularity": "day"
            },
            "time": {
                "type": "temporal", 
                "description": "Flight operation time",
                "granularity": "minute"
            },
            "region": {
                "type": "spatial",
                "description": "Operation district in Shenzhen",
                "categories": ["Baoan", "Longgang", "Futian", "Luohu", "Guangming", 
                              "Yantian", "Longhua", "Dapeng", "Nanshan", "Pingshan"]
            },
            "duration": {
                "type": "numerical",
                "description": "Flight duration in minutes",
                "unit": "minutes",
                "aggregation": ["sum", "avg", "max"]
            },
            "distance": {
                "type": "numerical",
                "description": "Flight distance in kilometers",
                "unit": "km",
                "aggregation": ["sum", "avg"]
            },
            "entity_id": {
                "type": "categorical",
                "description": "Operating enterprise identifier"
            },
            "entity": {
                "type": "categorical",
                "description": "Operating enterprise name"
            },
            "user_type": {
                "type": "categorical",
                "description": "Type of flight operator",
                "categories": ["企业用户", "个人用户", "未知用户"]
            },
            "aircraft_type": {
                "type": "categorical",
                "description": "Type of aircraft",
                "categories": ["MultiRotor", "FixedWing", "Helicopter"]
            },
            "aircraft_model": {
                "type": "categorical",
                "description": "Specific aircraft model",
                "categories": ["Mavic 3", "M300", "E200", "P100", "Dragonfish", "V50"]
            },
            "purpose": {
                "type": "categorical",
                "description": "Purpose of flight operation",
                "categories": ["Logistics", "Surveying", "Emergency", "Personal", "Inspection"]
            },
            "sn": {
                "type": "categorical",
                "description": "Aircraft serial number"
            },
            "altitude": {
                "type": "numerical",
                "description": "Maximum flight altitude in meters",
                "unit": "meters",
                "range": [0, 1000]
            },
            "start_region": {
                "type": "spatial",
                "description": "Departure district"
            },
            "end_region": {
                "type": "spatial",
                "description": "Arrival district"
            },
            "is_holiday": {
                "type": "categorical",
                "description": "Whether operation occurred on holiday",
                "categories": [True, False]
            },
            "is_planned": {
                "type": "categorical",
                "description": "Whether flight was planned",
                "categories": [True, False]
            },
            "is_effective": {
                "type": "categorical",
                "description": "Whether flight was completed effectively",
                "categories": [True, False]
            }
        }
    }
    
    def __init__(self):
        self.df: Optional[pd.DataFrame] = None
        self._load_data()
    
    def _load_data(self):
        """Load the real flight dataset"""
        if not self.DATA_PATH.exists():
            # Copy from python/data
            source = Path(__file__).parent.parent.parent / "python" / "data" / "sample_flight_data.csv"
            if source.exists():
                import shutil
                shutil.copy(source, self.DATA_PATH)
        
        if not self.DATA_PATH.exists():
            raise FileNotFoundError(f"Dataset not found at {self.DATA_PATH}")
        
        self.df = pd.read_csv(self.DATA_PATH)
        
        # Parse datetime
        self.df['datetime'] = pd.to_datetime(self.df['date'] + ' ' + self.df['time'])
        self.df['month'] = self.df['datetime'].dt.month
        self.df['hour'] = self.df['datetime'].dt.hour
        self.df['day_of_week'] = self.df['datetime'].dt.dayofweek
        
        print(f"Loaded LAEV Dataset: {len(self.df)} records, {len(self.df.columns)} attributes")
    
    def get_dataframe(self) -> pd.DataFrame:
        """Get the full dataset"""
        return self.df.copy()
    
    def get_nl4dv_format(self) -> pd.DataFrame:
        """
        Get data formatted for NL4DV baseline
        NL4DV expects specific column naming conventions
        """
        df_nl4dv = self.df.copy()
        # NL4DV works best with standard pandas DataFrame
        return df_nl4dv
    
    def get_sample(self, n: int = 100) -> pd.DataFrame:
        """Get a random sample for quick testing"""
        return self.df.sample(n=min(n, len(self.df)))
    
    def get_domain_metadata(self) -> Dict[str, Any]:
        """Get domain-specific metadata"""
        return self.DOMAIN_METADATA
    
    def validate_query_relevance(self, query: str) -> Dict[str, Any]:
        """
        Validate if a natural language query is relevant to this dataset
        Returns relevance score and matching attributes
        """
        query_lower = query.lower()
        
        # Check for temporal terms
        temporal_terms = ['时间', 'time', 'date', '日期', 'month', '月份', 'trend', '趋势', 'when']
        has_temporal = any(term in query_lower for term in temporal_terms)
        
        # Check for spatial terms
        spatial_terms = ['region', '区域', 'district', '地区', 'shenzhen', '深圳', 'where', 'location']
        has_spatial = any(term in query_lower for term in spatial_terms)
        
        # Check for categorical terms
        cat_terms = ['aircraft', '飞机', 'drone', '无人机', 'purpose', '目的', 'type', '类型']
        has_categorical = any(term in query_lower for term in cat_terms)
        
        # Check for numerical/measurement terms
        num_terms = ['duration', '时长', 'time', '距离', 'distance', 'altitude', '高度', 'count', '数量']
        has_numerical = any(term in query_lower for term in num_terms)
        
        # Calculate relevance
        relevance_score = sum([has_temporal, has_spatial, has_categorical, has_numerical]) / 4
        
        return {
            "relevance_score": relevance_score,
            "has_temporal": has_temporal,
            "has_spatial": has_spatial,
            "has_categorical": has_categorical,
            "has_numerical": has_numerical,
            "is_relevant": relevance_score > 0.25
        }


# Global dataset instance
_dataset_instance = None


def get_dataset() -> LAEVDataset:
    """Get singleton dataset instance"""
    global _dataset_instance
    if _dataset_instance is None:
        _dataset_instance = LAEVDataset()
    return _dataset_instance


if __name__ == "__main__":
    # Test the dataset loader
    dataset = LAEVDataset()
    print("\nDataset Info:")
    print(f"Shape: {dataset.df.shape}")
    print(f"\nFirst few rows:")
    print(dataset.df.head())
    print(f"\nDomain Metadata:")
    print(json.dumps(dataset.get_domain_metadata(), indent=2, ensure_ascii=False)[:1000])

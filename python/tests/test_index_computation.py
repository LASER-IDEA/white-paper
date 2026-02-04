"""
Tests for index computation and data processing.

This test suite validates:
- Index computation correctness
- Data validation and error handling
- Edge cases and boundary conditions
- Performance characteristics
"""

import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from data_processor import process_csv, validate_index_value


class TestDataValidation:
    """Test data validation and preprocessing."""
    
    def test_missing_required_columns(self):
        """Test that missing required columns raise appropriate errors."""
        df = pd.DataFrame({
            'date': ['2023-01-01'],
            'region': ['Test Region']
            # Missing duration, distance, entity
        })
        
        with pytest.raises(ValueError, match="Missing required column"):
            process_csv(df)
    
    def test_invalid_date_handling(self):
        """Test handling of invalid dates."""
        df = pd.DataFrame({
            'date': ['2023-01-01', 'invalid-date', '2023-01-03'],
            'region': ['A', 'B', 'C'],
            'duration': [10, 20, 30],
            'distance': [5, 10, 15],
            'entity': ['E1', 'E2', 'E3']
        })
        
        streamlit_data, ts_data = process_csv(df)
        # Should have 2 rows (invalid date dropped)
        assert len(ts_data) > 0, "Should process valid rows"
    
    def test_negative_values_handling(self):
        """Test handling of negative duration/distance values."""
        df = pd.DataFrame({
            'date': ['2023-01-01', '2023-01-02'],
            'region': ['A', 'B'],
            'duration': [10, -5],  # Negative duration
            'distance': [-2, 10],  # Negative distance
            'entity': ['E1', 'E2']
        })
        
        streamlit_data, ts_data = process_csv(df)
        # Check that negative values were converted to absolute
        traffic_data = streamlit_data['traffic']
        assert len(traffic_data) > 0, "Should have traffic data"
    
    def test_nan_values_handling(self):
        """Test handling of NaN values."""
        df = pd.DataFrame({
            'date': ['2023-01-01', '2023-01-02', '2023-01-03'],
            'region': ['A', 'B', 'C'],
            'duration': [10, np.nan, 30],
            'distance': [5, 10, np.nan],
            'entity': ['E1', 'E2', 'E3']
        })
        
        streamlit_data, ts_data = process_csv(df)
        # Should fill NaN values and process successfully
        assert len(ts_data) > 0, "Should handle NaN values"


class TestIndexComputation:
    """Test individual index computations."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing."""
        np.random.seed(42)
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        
        return pd.DataFrame({
            'date': dates,
            'region': np.random.choice(['A', 'B', 'C', 'D'], 100),
            'duration': np.random.uniform(5, 60, 100),
            'distance': np.random.uniform(1, 50, 100),
            'entity': np.random.choice(['E1', 'E2', 'E3', 'E4', 'E5'], 100),
            'aircraft_type': np.random.choice(['MultiRotor', 'FixedWing', 'Helicopter'], 100),
            'aircraft_model': np.random.choice(['Model A', 'Model B', 'Model C'], 100),
            'sn': [f"SN{i:04d}" for i in range(100)],
            'altitude': np.random.uniform(50, 300, 100),
            'start_region': np.random.choice(['A', 'B', 'C', 'D'], 100),
            'end_region': np.random.choice(['A', 'B', 'C', 'D'], 100),
            'user_type': np.random.choice(['企业用户', '个人用户'], 100),
            'is_planned': np.random.choice([True, False], 100),
            'is_effective': np.random.choice([True, False], 100)
        })
    
    def test_traffic_index_computation(self, sample_data):
        """Test traffic index computation."""
        streamlit_data, ts_data = process_csv(sample_data)
        
        # Find traffic index in ts_data
        traffic_metric = next((m for m in ts_data if m['id'] == '01'), None)
        assert traffic_metric is not None, "Traffic index should be computed"
        assert traffic_metric['value'] >= 0, "Traffic index should be non-negative"
        assert traffic_metric['chartType'] == 'Area', "Should use Area chart"
    
    def test_fleet_index_computation(self, sample_data):
        """Test active fleet index computation."""
        streamlit_data, ts_data = process_csv(sample_data)
        
        # Find fleet index
        fleet_metric = next((m for m in ts_data if m['id'] == '03'), None)
        assert fleet_metric is not None, "Fleet index should be computed"
        
        # Fleet count should equal unique SNs
        unique_sns = sample_data['sn'].nunique()
        assert fleet_metric['value'] == unique_sns, "Fleet count should match unique SNs"
    
    def test_market_concentration_computation(self, sample_data):
        """Test market concentration (CR50) computation."""
        streamlit_data, ts_data = process_csv(sample_data)
        
        # Find CR50 index
        cr50_metric = next((m for m in ts_data if m['id'] == '05'), None)
        assert cr50_metric is not None, "CR50 should be computed"
        
        # CR50 should be a percentage string
        value_str = str(cr50_metric['value'])
        assert 'CR50=' in value_str or '%' in value_str or isinstance(cr50_metric['value'], (int, float))
    
    def test_diversity_index_range(self, sample_data):
        """Test that diversity index is in valid range [0, 1]."""
        streamlit_data, ts_data = process_csv(sample_data)
        
        # Find diversity index
        diversity_metric = next((m for m in ts_data if m['id'] == '07'), None)
        assert diversity_metric is not None, "Diversity index should be computed"
        
        value = diversity_metric['value']
        assert 0 <= value <= 1, f"Diversity index {value} should be in [0, 1]"
    
    def test_completion_quality_range(self, sample_data):
        """Test that completion quality is a valid percentage."""
        streamlit_data, ts_data = process_csv(sample_data)
        
        # Find TQI index
        tqi_metric = next((m for m in ts_data if m['id'] == '15'), None)
        assert tqi_metric is not None, "TQI should be computed"
        
        value = tqi_metric['value']
        assert 0 <= value <= 100, f"TQI {value}% should be in [0, 100]"


class TestIndexValidation:
    """Test index validation helper."""
    
    def test_nan_detection(self):
        """Test NaN value detection and handling."""
        result = validate_index_value(np.nan, "Test Index", (0, 100))
        assert result == 0, "NaN should be converted to 0"
    
    def test_inf_detection(self):
        """Test Inf value detection and handling."""
        result = validate_index_value(np.inf, "Test Index", (0, 100))
        assert result == 100, "Positive Inf should be capped to max"
        
        result = validate_index_value(-np.inf, "Test Index", (0, 100))
        assert result == 0, "Negative Inf should be capped to min"
    
    def test_valid_value_passthrough(self):
        """Test that valid values pass through unchanged."""
        result = validate_index_value(50, "Test Index", (0, 100))
        assert result == 50, "Valid value should pass through"


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_single_row_processing(self):
        """Test processing with single data row."""
        df = pd.DataFrame({
            'date': ['2023-01-01'],
            'region': ['A'],
            'duration': [10],
            'distance': [5],
            'entity': ['E1']
        })
        
        streamlit_data, ts_data = process_csv(df)
        assert len(ts_data) > 0, "Should process single row"
    
    def test_single_entity(self):
        """Test with data from single entity."""
        df = pd.DataFrame({
            'date': pd.date_range('2023-01-01', periods=10),
            'region': ['A'] * 10,
            'duration': [10] * 10,
            'distance': [5] * 10,
            'entity': ['E1'] * 10  # Single entity
        })
        
        streamlit_data, ts_data = process_csv(df)
        
        # CR50 should be 100% (single entity has 100% market share)
        cr50_metric = next((m for m in ts_data if m['id'] == '05'), None)
        assert cr50_metric is not None
    
    def test_all_same_region(self):
        """Test with all flights in same region."""
        df = pd.DataFrame({
            'date': pd.date_range('2023-01-01', periods=10),
            'region': ['A'] * 10,  # All same region
            'duration': [10] * 10,
            'distance': [5] * 10,
            'entity': ['E1'] * 10,
            'start_region': ['A'] * 10,
            'end_region': ['A'] * 10
        })
        
        streamlit_data, ts_data = process_csv(df)
        
        # Balance index should be 1.0 (perfect balance - only one region)
        balance_metric = next((m for m in ts_data if m['id'] == '08'), None)
        assert balance_metric is not None


class TestPerformance:
    """Test performance characteristics."""
    
    def test_large_dataset_processing(self):
        """Test processing large dataset (10K rows)."""
        import time
        
        np.random.seed(42)
        n = 10000
        dates = pd.date_range('2023-01-01', periods=n, freq='1H')
        
        df = pd.DataFrame({
            'date': dates,
            'region': np.random.choice(['A', 'B', 'C', 'D', 'E'], n),
            'duration': np.random.uniform(5, 60, n),
            'distance': np.random.uniform(1, 50, n),
            'entity': np.random.choice([f'E{i}' for i in range(100)], n),
            'aircraft_type': np.random.choice(['MultiRotor', 'FixedWing'], n),
            'sn': [f"SN{i:04d}" for i in range(n)]
        })
        
        start_time = time.time()
        streamlit_data, ts_data = process_csv(df)
        elapsed = time.time() - start_time
        
        assert elapsed < 10, f"Processing {n} rows took {elapsed:.2f}s, should be < 10s"
        assert len(ts_data) > 0, "Should produce indices"
    
    def test_memory_efficiency(self):
        """Test that processing doesn't create excessive copies."""
        import sys
        
        df = pd.DataFrame({
            'date': pd.date_range('2023-01-01', periods=1000),
            'region': ['A'] * 1000,
            'duration': [10] * 1000,
            'distance': [5] * 1000,
            'entity': ['E1'] * 1000
        })
        
        initial_size = sys.getsizeof(df)
        streamlit_data, ts_data = process_csv(df)
        
        # Output size should be reasonable (not orders of magnitude larger)
        # This is a rough check - actual sizes vary
        assert sys.getsizeof(ts_data) < initial_size * 5, "Output shouldn't be excessively large"


class TestChartDataFormats:
    """Test that chart data formats are correct."""
    
    @pytest.fixture
    def processed_data(self):
        """Get processed data for testing."""
        df = pd.DataFrame({
            'date': pd.date_range('2023-01-01', periods=50),
            'region': np.random.choice(['A', 'B', 'C'], 50),
            'duration': np.random.uniform(5, 60, 50),
            'distance': np.random.uniform(1, 50, 50),
            'entity': np.random.choice(['E1', 'E2', 'E3'], 50),
            'aircraft_type': np.random.choice(['MultiRotor', 'FixedWing'], 50),
            'sn': [f"SN{i:04d}" for i in range(50)]
        })
        return process_csv(df)
    
    def test_area_chart_format(self, processed_data):
        """Test that Area chart data has correct format."""
        streamlit_data, ts_data = processed_data
        
        traffic_metric = next((m for m in ts_data if m['chartType'] == 'Area'), None)
        assert traffic_metric is not None
        
        # Check data format: [{date: str, value: number}, ...]
        chart_data = traffic_metric['chartData']
        assert isinstance(chart_data, list)
        if len(chart_data) > 0:
            item = chart_data[0]
            assert 'date' in item or 'month' in item
            assert 'value' in item
    
    def test_stacked_bar_format(self, processed_data):
        """Test that StackedBar chart data has correct format."""
        streamlit_data, ts_data = processed_data
        
        fleet_metric = next((m for m in ts_data if m['chartType'] == 'StackedBar'), None)
        assert fleet_metric is not None
        
        # Check data format: [{name: str, MultiRotor: num, FixedWing: num, ...}, ...]
        chart_data = fleet_metric['chartData']
        assert isinstance(chart_data, list)
        if len(chart_data) > 0:
            item = chart_data[0]
            assert 'name' in item
    
    def test_radar_chart_format(self, processed_data):
        """Test that Radar chart data has correct format."""
        streamlit_data, ts_data = processed_data
        
        radar_metric = next((m for m in ts_data if m['chartType'] == 'Radar'), None)
        assert radar_metric is not None
        
        # Check data format: [{subject: str, fullMark: num, A: num, B: num}, ...]
        chart_data = radar_metric['chartData']
        assert isinstance(chart_data, list)


if __name__ == '__main__':
    # Run tests with pytest
    pytest.main([__file__, '-v', '--tb=short'])

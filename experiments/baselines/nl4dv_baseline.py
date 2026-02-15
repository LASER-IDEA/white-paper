"""
NL4DV Baseline Implementation
Wraps NL4DV toolkit for fair comparison
"""

import sys
sys.path.insert(0, '/data1/xh/workspace/white-paper/nl4dv')

import json
import time
from typing import Dict, Any, Optional, List
import pandas as pd


class NL4DVBaseline:
    """
    NL4DV Baseline wrapper for comparison experiments.
    
    NL4DV (Natural Language toolkit for Data Visualization) by Georgia Tech
    converts natural language queries to Vega-Lite specifications.
    
    Paper: Narechania et al., "NL4DV: A Toolkit for Generating Analytic Specifications 
           for Data Visualization from Natural Language Queries", IEEE TVCG 2021
    """
    
    def __init__(self, dataset_path: Optional[str] = None):
        """
        Initialize NL4DV baseline
        
        Args:
            dataset_path: Path to CSV dataset file
        """
        self.nl4dv = None
        self.dataset_path = dataset_path
        self.execution_logs: List[Dict] = []
        self.nl4dv_module = None
        
        try:
            from nl4dv import NL4DV
            self.nl4dv_module = NL4DV
            
            if dataset_path:
                self.load_dataset(dataset_path)
                
        except ImportError as e:
            print(f"Warning: Could not import NL4DV: {e}")
            print("Please install: pip install nl4dv")
    
    def load_dataset(self, dataset_path: str) -> bool:
        """Load dataset into NL4DV"""
        if self.nl4dv_module is None:
            return False
        
        try:
            # Create NL4DV instance with data URL
            self.nl4dv = self.nl4dv_module(data_url=dataset_path)
            self.dataset_path = dataset_path
            return True
        except Exception as e:
            print(f"Error loading dataset: {e}")
            return False
    
    def load_dataframe(self, df: pd.DataFrame, label: str = "data") -> bool:
        """Load pandas DataFrame into NL4DV"""
        if self.nl4dv_module is None:
            return False
        
        try:
            # Save to temp CSV for NL4DV
            import tempfile
            import os
            
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, f"nl4dv_{label}.csv")
            df.to_csv(temp_path, index=False)
            
            # Create NL4DV instance with data URL
            self.nl4dv = self.nl4dv_module(data_url=temp_path)
            self.dataset_path = temp_path
            return True
            
        except Exception as e:
            print(f"Error loading dataframe: {e}")
            return False
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process a natural language query
        
        Args:
            query: Natural language query
            
        Returns:
            Result dictionary with Vega-Lite spec and metadata
        """
        if self.nl4dv is None:
            return {
                "success": False,
                "error": "NL4DV not initialized",
                "query": query,
                "vega_spec": None,
                "execution_time": 0
            }
        
        start_time = time.time()
        
        try:
            # Execute NL4DV
            result = self.nl4dv.analyze_query(query)
            
            execution_time = time.time() - start_time
            
            # Parse result
            vis_list = result.get('visList', [])
            
            if not vis_list:
                return {
                    "success": False,
                    "error": "No visualization generated",
                    "query": query,
                    "vega_spec": None,
                    "execution_time": execution_time,
                    "raw_result": result
                }
            
            # Get top visualization
            top_vis = vis_list[0]
            vega_spec = top_vis.get('vlSpec', {})
            
            log_entry = {
                "query": query,
                "execution_time": execution_time,
                "success": True,
                "chart_type": self._extract_chart_type(vega_spec)
            }
            self.execution_logs.append(log_entry)
            
            return {
                "success": True,
                "error": None,
                "query": query,
                "vega_spec": vega_spec,
                "chart_type": self._extract_chart_type(vega_spec),
                "execution_time": execution_time,
                "all_visualizations": len(vis_list),
                "raw_result": result
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            log_entry = {
                "query": query,
                "execution_time": execution_time,
                "success": False,
                "error": str(e)
            }
            self.execution_logs.append(log_entry)
            
            return {
                "success": False,
                "error": str(e),
                "query": query,
                "vega_spec": None,
                "execution_time": execution_time
            }
    
    def _extract_chart_type(self, vega_spec: Dict) -> str:
        """Extract chart type from Vega-Lite spec"""
        mark = vega_spec.get('mark', {})
        if isinstance(mark, dict):
            return mark.get('type', 'unknown')
        elif isinstance(mark, str):
            return mark
        return 'unknown'
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get execution statistics"""
        if not self.execution_logs:
            return {
                "total_queries": 0,
                "success_rate": 0,
                "avg_execution_time": 0
            }
        
        total = len(self.execution_logs)
        successful = sum(1 for log in self.execution_logs if log.get('success'))
        avg_time = sum(log.get('execution_time', 0) for log in self.execution_logs) / total
        
        return {
            "total_queries": total,
            "successful": successful,
            "success_rate": successful / total if total > 0 else 0,
            "avg_execution_time": avg_time
        }


class DirectLLMBaseline:
    """
    Direct LLM Baseline - queries LLM without RAG or Multi-Agent
    Simulates naive approach: query -> LLM -> code
    """
    
    def __init__(self, llm_provider: str = "deepseek"):
        self.llm_provider = llm_provider
        self.execution_logs: List[Dict] = []
    
    def process_query(self, query: str, data_schema: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Process query using direct LLM prompting
        
        Args:
            query: Natural language query
            data_schema: Optional data schema information
            
        Returns:
            Result dictionary
        """
        import time
        import sys
        sys.path.insert(0, '/data1/xh/workspace/white-paper/python/src')
        start_time = time.time()
        
        try:
            from llm_client import LLMClient
            
            llm = LLMClient(provider=self.llm_provider)
            
            # Simple prompt without context
            system_prompt = """You are a data visualization expert. 
Generate Python code using PyECharts based on the user's query.
Return ONLY the code, no explanations."""
            
            user_prompt = f"Query: {query}"
            if data_schema:
                user_prompt += f"\n\nAvailable data columns: {list(data_schema.keys())}"
            
            response = llm.generate(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=0.3
            )
            
            # Extract code (simple version)
            code = response
            if '```python' in response:
                code = response.split('```python')[1].split('```')[0]
            elif '```' in response:
                code = response.split('```')[1].split('```')[0]
            
            execution_time = time.time() - start_time
            
            log_entry = {
                "query": query,
                "execution_time": execution_time,
                "success": True
            }
            self.execution_logs.append(log_entry)
            
            return {
                "success": True,
                "error": None,
                "query": query,
                "generated_code": code.strip(),
                "execution_time": execution_time
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            return {
                "success": False,
                "error": str(e),
                "query": query,
                "generated_code": None,
                "execution_time": execution_time
            }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get execution statistics"""
        if not self.execution_logs:
            return {
                "total_queries": 0,
                "success_rate": 0,
                "avg_execution_time": 0
            }
        
        total = len(self.execution_logs)
        successful = sum(1 for log in self.execution_logs if log.get('success'))
        avg_time = sum(log.get('execution_time', 0) for log in self.execution_logs) / total
        
        return {
            "total_queries": total,
            "successful": successful,
            "success_rate": successful / total if total > 0 else 0,
            "avg_execution_time": avg_time
        }


if __name__ == "__main__":
    # Test NL4DV baseline
    print("Testing NL4DV Baseline...")
    
    # Initialize with dataset
    dataset_path = "/data1/xh/workspace/white-paper/python/data/sample_flight_data.csv"
    baseline = NL4DVBaseline(dataset_path)
    
    # Test queries
    test_queries = [
        "Show flight duration by region",
        "What is the trend of flights over time?",
        "Compare different aircraft types"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        result = baseline.process_query(query)
        print(f"Success: {result['success']}")
        if result['success']:
            print(f"Chart Type: {result['chart_type']}")
        else:
            print(f"Error: {result['error']}")
    
    print("\nStatistics:")
    print(json.dumps(baseline.get_statistics(), indent=2))

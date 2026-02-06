"""
Generate TypeScript data file for web report from computed metrics.

This script reads the computed metrics JSON and generates a TypeScript file
that can be used directly in the web application.

Usage:
    python generate_web_data.py --input output/metrics.json --output ../web/src/utils/computedData.ts
"""

import json
import argparse
from pathlib import Path
from typing import List, Dict, Any


def generate_typescript(metrics: List[Dict[str, Any]], output_file: str):
    """Generate TypeScript file from metrics data."""
    
    # Map Chinese dimensions to TypeScript Dimension enum
    dimension_map = {
        "规模与增长": "Dimension.ScaleGrowth",
        "结构与主体": "Dimension.StructureEntity",
        "时空特征": "Dimension.TimeSpace",
        "效率与质量": "Dimension.EfficiencyQuality",
        "创新与融合": "Dimension.InnovationIntegration"
    }
    
    # Group metrics by dimension
    scale_growth = [m for m in metrics if m['dimension'] == '规模与增长']
    structure_entity = [m for m in metrics if m['dimension'] == '结构与主体']
    time_space = [m for m in metrics if m['dimension'] == '时空特征']
    efficiency_quality = [m for m in metrics if m['dimension'] == '效率与质量']
    innovation = [m for m in metrics if m['dimension'] == '创新与融合']
    
    def format_value(v):
        """Format a value for TypeScript."""
        if isinstance(v, str):
            # Escape single quotes
            escaped = v.replace("'", "\\'")
            return f"'{escaped}'"
        elif isinstance(v, bool):
            return 'true' if v else 'false'
        elif isinstance(v, (int, float)):
            return str(v)
        elif v is None:
            return 'null'
        else:
            return json.dumps(v, ensure_ascii=False)
    
    def format_chart_data(data: Any, indent: int = 4) -> str:
        """Format chart data in compact TypeScript format matching mockData.ts style."""
        if isinstance(data, list):
            if not data:
                return '[]'
            items = []
            for item in data:
                if isinstance(item, dict):
                    # Format as single line: { key: value, key: value }
                    item_str = '{ ' + ', '.join(
                        f"{k}: {format_value(v)}" for k, v in item.items()
                    ) + ' }'
                    items.append(item_str)
                else:
                    items.append(format_value(item))
            # Format like mockData.ts: each item on its own line with proper indentation
            return '[\n' + ',\n'.join(' ' * indent + item for item in items) + '\n' + ' ' * (indent - 2) + ']'
        elif isinstance(data, dict):
            items = []
            for k, v in data.items():
                if isinstance(v, list):
                    items.append(f"{k}: {format_chart_data(v, indent + 2)}")
                elif isinstance(v, dict):
                    items.append(f"{k}: {format_chart_data(v, indent + 2)}")
                else:
                    items.append(f"{k}: {format_value(v)}")
            return '{\n' + ',\n'.join(' ' * indent + item for item in items) + '\n' + ' ' * (indent - 2) + '}'
        else:
            return format_value(data)
    
    def format_key_metrics(metrics: List[Dict]) -> str:
        """Format key metrics in compact format matching mockData.ts style."""
        if not metrics:
            return '[]'
        items = []
        for m in metrics:
            items.append(f"{{ label: {format_value(m['label'])}, value: {format_value(m['value'])} }}")
        # Format like mockData.ts: each item on its own line with proper indentation
        return '[\n' + ',\n'.join(' ' * 4 + item for item in items) + '\n    ]'
    
    def format_metric(m: Dict[str, Any]) -> str:
        """Format a single metric object for TypeScript."""
        dim = dimension_map.get(m['dimension'], 'Dimension.ScaleGrowth')
        
        # Format chart data
        chart_data = format_chart_data(m['chartData'], indent=4)
        
        # Format key metrics
        key_metrics = format_key_metrics(m.get('keyMetrics', []))
        
        # Escape single quotes in strings
        def escape_quotes(s):
            return s.replace("'", "\\'") if s else ""
        
        definition = escape_quotes(m["definition"])
        insight = escape_quotes(m.get("insight", ""))
        suggestion = escape_quotes(m.get("suggestion", ""))
        
        return f"""  {{
    id: '{m["id"]}',
    title: '{m["title"]}',
    subtitle: '{m["subtitle"]}',
    dimension: {dim},
    value: {format_value(m["value"])},
    unit: '{m["unit"]}',
    trend: {m.get("trend", 0)},
    definition: '{definition}',
    insight: '{insight}',
    suggestion: '{suggestion}',
    chartType: '{m["chartType"]}',
    chartData: {chart_data},
    keyMetrics: {key_metrics}
  }}"""
    
    def format_group(group: List[Dict], name: str) -> str:
        """Format a group of metrics as a function."""
        if not group:
            return f"export const get{name}Data = (): MetricData[] => [];\n"
        
        items = ',\n'.join(format_metric(m) for m in group)
        return f"""export const get{name}Data = (): MetricData[] => [
{items}
];
"""
    
    # Generate TypeScript file content
    ts_content = f"""/**
 * Computed metrics data from markdown files.
 * Generated automatically - do not edit manually.
 * 
 * To regenerate this file:
 *   python markdown_processor.py --input data/example.md --output output/metrics.json
 *   python generate_web_data.py --input output/metrics.json --output ../web/src/utils/computedData.ts
 */

import {{ Dimension, MetricData }} from '../types';

// 1. Scale & Growth
{format_group(scale_growth, 'ScaleGrowth')}

// 2. Structure & Entity
{format_group(structure_entity, 'StructureEntity')}

// 3. Time & Space
{format_group(time_space, 'TimeSpace')}

// 4. Efficiency & Quality
{format_group(efficiency_quality, 'EfficiencyQuality')}

// 5. Innovation & Integration
{format_group(innovation, 'Innovation')}

export const getAllComputedData = (): MetricData[] => [
  ...getScaleGrowthData(),
  ...getStructureEntityData(),
  ...getTimeSpaceData(),
  ...getEfficiencyQualityData(),
  ...getInnovationData(),
];
"""
    
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(ts_content)
    
    print(f"TypeScript file generated: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description='Generate TypeScript data file from computed metrics.'
    )
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Input JSON file with computed metrics'
    )
    parser.add_argument(
        '--output', '-o',
        default='../web/src/utils/computedData.ts',
        help='Output TypeScript file (default: ../web/src/utils/computedData.ts)'
    )
    
    args = parser.parse_args()
    
    if not Path(args.input).exists():
        print(f"Error: Input file not found: {args.input}")
        return 1
    
    with open(args.input, 'r', encoding='utf-8') as f:
        metrics = json.load(f)
    
    generate_typescript(metrics, args.output)
    return 0


if __name__ == '__main__':
    exit(main())

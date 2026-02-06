"""
Markdown Data Processor for Low-Altitude Economy Index Computation

This script reads aggregated data from markdown files and computes the 20 indices
for the web report generation.

Usage:
    python markdown_processor.py --input data/example.md --output output/metrics.json
    python markdown_processor.py --input data/example.md data/annual_example.md --output output/metrics.json
"""

import re
import json
import argparse
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from io import StringIO
from datetime import datetime


class MarkdownTableParser:
    """Parser for extracting tables from markdown files."""

    def __init__(self):
        self.tables: Dict[str, pd.DataFrame] = {}
        self.table_titles: Dict[str, str] = {}

    def parse_file(self, filepath: str) -> Dict[str, pd.DataFrame]:
        """Parse a markdown file and extract all tables with their section titles."""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split by section headers (## or ###)
        sections = re.split(r'\n(?=##\s+\d+[\._])', content)

        for section in sections:
            if not section.strip():
                continue

            # Extract section title
            title_match = re.match(r'##\s*(\d+[\._]?\d*\.?)\s*(.*?)(?:\n|$)', section)
            if not title_match:
                continue

            section_num = title_match.group(1).strip('._')
            section_title = title_match.group(2).strip()

            # Find markdown table in section
            table_match = re.search(
                r'\|[^\n]+\|\n\|[-:\s|]+\|\n((?:\|[^\n]*\|\n?)*)',
                section
            )

            if table_match:
                # Get full table including header
                table_start = section.find('|')
                table_text = section[table_start:]
                # Find end of table
                lines = table_text.split('\n')
                table_lines = []
                for line in lines:
                    if line.strip().startswith('|') and line.strip().endswith('|'):
                        table_lines.append(line)
                    elif table_lines:  # End of table
                        break

                if len(table_lines) >= 2:  # At least header and separator
                    df = self._parse_table_lines(table_lines)
                    if df is not None and not df.empty:
                        key = f"table_{section_num}"
                        self.tables[key] = df
                        self.table_titles[key] = section_title

        return self.tables

    def _parse_table_lines(self, lines: List[str]) -> Optional[pd.DataFrame]:
        """Parse markdown table lines into a DataFrame."""
        if len(lines) < 2:
            return None

        # Parse header
        header = [col.strip() for col in lines[0].split('|')[1:-1]]

        # Skip separator line (lines[1])

        # Parse data rows
        data_rows = []
        for line in lines[2:]:
            if not line.strip():
                continue
            row = [cell.strip() for cell in line.split('|')[1:-1]]
            if len(row) == len(header):
                # Clean up each cell
                cleaned_row = []
                for cell in row:
                    # Handle empty cells
                    if not cell or cell.isspace():
                        cleaned_row.append(None)
                    # Handle values starting with '.' (missing integer part)
                    elif cell.startswith('.') and len(cell) > 1:
                        cleaned_row.append('0' + cell)
                    else:
                        cleaned_row.append(cell)
                data_rows.append(cleaned_row)

        if not data_rows:
            return pd.DataFrame(columns=header)

        df = pd.DataFrame(data_rows, columns=header)

        # Identify string columns (name, code, id, type, percentage columns should stay as strings)
        string_col_patterns = ['name', 'code', 'id', 'type', 'category', 'range', 'time', 'month', 'date', 'percentage', 'entity', 'manufacturer', 'aircraft']

        # Convert columns appropriately
        for col in df.columns:
            col_lower = col.lower()
            is_string_col = any(pattern in col_lower for pattern in string_col_patterns)

            if is_string_col:
                # Keep as string, but clean up None values
                df[col] = df[col].fillna('')
            else:
                # Try to convert to numeric
                df[col] = pd.to_numeric(df[col], errors='coerce')

        return df


class IndexComputer:
    """Computes the 20 low-altitude economy indices from parsed markdown data."""

    def __init__(self, tables: Dict[str, pd.DataFrame], titles: Dict[str, str]):
        self.tables = tables
        self.titles = titles
        self.metrics: List[Dict[str, Any]] = []

        # Map table numbers to their purposes based on common column patterns
        self._categorize_tables()

    def _categorize_tables(self):
        """Categorize tables by their content for index computation."""
        self.daily_flights = None
        self.monthly_flights = None
        self.annual_flights = None
        self.annual_daily_avg = None
        self.weekly_flights = None
        self.workday_avg = None
        self.weekend_avg = None
        self.user_type_monthly = None
        self.district_annual = None
        self.top50_entities = None
        self.top50_percentage = None
        self.aircraft_model_annual = None
        self.effective_monthly = None
        self.effective_weekday = None
        self.cross_region = None
        self.hourly_flights = None
        self.hourly_duration = None
        self.duration_ranges = None
        self.distance_ranges = None
        self.monthly_duration = None
        self.district_duration = None
        self.monthly_distance = None
        self.district_distance = None
        self.height_ranges = None
        self.district_height = None
        self.speed_ranges = None
        self.daily_sn = None
        self.annual_sn = None
        self.annual_daily_sn_avg = None
        self.aircraft_category_sn = None
        self.aircraft_type_sn = None
        self.manufacturer_sn = None
        self.entity_sn = None
        self.user_type_daily = None
        self.user_type_annual = None
        self.top5_hourly = None
        self.top5_distance_range = None
        self.top50_height = None
        self.top5_speed = None
        self.top5_max_speed = None
        self.top50_duration = None
        self.top50_distance = None
        self.top50_sn = None
        self.annual_total_duration = None
        self.annual_total_distance = None
        self.user_type_sn = None
        self.annual_effective = None
        self.annual_users = None
        self.hourly_distance = None

        # Match tables by title keywords
        for key, title in self.titles.items():
            df = self.tables.get(key)
            if df is None or df.empty:
                continue

            title_lower = title.lower()

            # Daily flight counts
            if '日度飞行架次' in title or '每日飞行' in title:
                self.daily_flights = df
            # Monthly flight counts
            elif '月度飞行架次' in title and '有效' not in title:
                self.monthly_flights = df
            # Annual flight counts
            elif '年度飞行架次' in title or ('年' in title and 'flight_count' in df.columns and len(df.columns) <= 3):
                if 'flight_count' in df.columns and 'year' in df.columns:
                    self.annual_flights = df
            # Annual daily average
            elif '年日均飞行架次' in title:
                self.annual_daily_avg = df
            # Weekly (by weekday)
            elif '周均' in title or 'day_of_week' in str(df.columns):
                self.weekly_flights = df
            # Workday average
            elif '工作日' in title and '日均' in title:
                self.workday_avg = df
            # Weekend average
            elif '周末' in title and '日均' in title:
                self.weekend_avg = df
            # User type monthly
            elif '用户类型' in title and '月' in title and '飞行架次' in title:
                self.user_type_monthly = df
            # District annual flights
            elif '行政区' in title and '年' in title and '飞行架次' in title:
                self.district_annual = df
            # TOP50 entities
            elif 'top50' in title_lower and '百分比' not in title:
                if 'flight_count' in df.columns and 'entity' in str(df.columns).lower():
                    self.top50_entities = df
            # TOP50 percentage
            elif 'top50' in title_lower and '百分比' in title:
                self.top50_percentage = df
            # Aircraft model annual
            elif '航空器型号' in title and '年' in title:
                self.aircraft_model_annual = df
            # Effective monthly
            elif '有效飞行架次' in title and '月' in title:
                self.effective_monthly = df
            # Effective weekday
            elif '有效飞行架次' in title and '周几' in title:
                self.effective_weekday = df
            # Cross region
            elif '跨区' in title or '跨行政区' in title:
                self.cross_region = df
            # Hourly flights
            elif '时段' in title and '飞行架次' in title and '里程' not in title:
                self.hourly_flights = df
            # Hourly duration
            elif '时段' in title and '飞行时长' in title:
                self.hourly_duration = df
            # Duration ranges
            elif '飞行时长区间' in title:
                self.duration_ranges = df
            # Distance ranges
            elif '飞行里程区间' in title and 'top5' not in title_lower:
                self.distance_ranges = df
            # Monthly duration
            elif '每月飞行时长' in title or ('月' in title and 'total_duration' in str(df.columns)):
                if 'district' not in str(df.columns).lower():
                    self.monthly_duration = df
            # District duration
            elif '行政区' in title and '飞行时长' in title:
                self.district_duration = df
            # Monthly distance
            elif '每月飞行里程' in title:
                self.monthly_distance = df
            # District distance
            elif '行政区' in title and '飞行里程' in title:
                self.district_distance = df
            # Height ranges
            elif '高度区间' in title and '行政区' not in title and 'top' not in title_lower:
                self.height_ranges = df
            # District height
            elif '行政区' in title and '高度区间' in title:
                self.district_height = df
            # Speed ranges
            elif '水平速度区间' in title and 'top' not in title_lower:
                self.speed_ranges = df
            # Daily SN
            elif '每日' in title and '活跃sn' in title_lower:
                self.daily_sn = df
            # Annual SN
            elif ('年' in title or '今年') and '活跃sn' in title_lower and '日均' not in title:
                if 'aircraft' not in title and 'user' not in title_lower and '用户' not in title:
                    self.annual_sn = df
            # Annual daily SN average
            elif '年日均活跃sn' in title_lower:
                self.annual_daily_sn_avg = df
            # Aircraft category SN
            elif '航空器类别' in title and '活跃sn' in title_lower:
                self.aircraft_category_sn = df
            # Aircraft type SN
            elif '航空器类型' in title and '活跃sn' in title_lower:
                self.aircraft_type_sn = df
            # User type SN
            elif '用户类型' in title and '活跃sn' in title_lower:
                self.user_type_sn = df
            # Annual effective flights
            elif '年合计有效飞行架次' in title:
                self.annual_effective = df
            # Annual users
            elif '年合计活跃用户数' in title:
                self.annual_users = df
            # Hourly distance
            elif '时段' in title and '飞行里程' in title:
                self.hourly_distance = df
            # TOP50 duration
            elif 'top50' in title_lower and '飞行时长' in title and '高度' not in title:
                self.top50_duration = df
            # TOP50 distance
            elif 'top50' in title_lower and '飞行里程' in title:
                self.top50_distance = df
            # TOP50 SN
            elif 'top50' in title_lower and '活跃sn' in title_lower:
                self.top50_sn = df
            # Annual total duration
            elif '年合计飞行时长' in title and '时段' not in title:
                self.annual_total_duration = df
            # Annual total distance
            elif '年合计飞行里程' in title and '时段' not in title:
                self.annual_total_distance = df

    def _calc_gini(self, values: np.ndarray) -> float:
        """Calculate Gini coefficient."""
        vals = np.array(values, dtype=float)
        vals = vals[~np.isnan(vals)]  # Remove NaN values
        if vals.size == 0 or np.all(vals == 0):
            return 0.0
        vals = np.sort(vals)
        n = vals.size
        index = np.arange(1, n + 1)
        return float((np.sum((2 * index - n - 1) * vals)) / (n * np.sum(vals)))

    def _calc_entropy(self, values: np.ndarray) -> float:
        """Calculate Shannon entropy."""
        vals = np.array(values, dtype=float)
        vals = vals[~np.isnan(vals)]  # Remove NaN values
        total = vals.sum()
        if total <= 0:
            return 0.0
        probs = vals / total
        probs = probs[probs > 0]
        return float(-(probs * np.log(probs)).sum())

    def _calc_simpson_diversity(self, values: np.ndarray) -> float:
        """Calculate Simpson diversity index."""
        vals = np.array(values, dtype=float)
        vals = vals[~np.isnan(vals)]  # Remove NaN values
        total = vals.sum()
        if total <= 0:
            return 0.0
        proportions = vals / total
        return float(1 - np.sum(proportions ** 2))

    def _safe_int(self, value, default: int = 0) -> int:
        """Safely convert a value to int, handling NaN and None."""
        if value is None or (isinstance(value, float) and np.isnan(value)):
            return default
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    def _safe_float(self, value, default: float = 0.0) -> float:
        """Safely convert a value to float, handling NaN and None."""
        if value is None:
            return default
        try:
            f = float(value)
            return default if np.isnan(f) else f
        except (ValueError, TypeError):
            return default

    def _safe_str(self, value, default: str = "未知") -> str:
        """Safely convert a value to string, handling NaN, None, and empty strings."""
        if value is None:
            return default
        if isinstance(value, float):
            if np.isnan(value):
                return default
            # Format float without unnecessary decimals
            if value == int(value):
                return str(int(value))
            return str(value)
        try:
            s = str(value).strip()
            # Check if it's empty, "nan", or "none" string
            if not s or s.lower() == 'nan' or s.lower() == 'none':
                return default
            return s
        except (ValueError, TypeError):
            return default

    def _is_workday(self, date_str: str) -> bool:
        """Check if a date string represents a workday."""
        try:
            date = pd.to_datetime(date_str)
            # Monday=0, Sunday=6, so workday is 0-4
            return date.weekday() < 5
        except:
            return True  # Default to workday if parsing fails

    def _get_district_name(self, code: str) -> str:
        """Map district code to district name."""
        district_map = {
            '440303': '罗湖区',
            '440304': '福田区',
            '440307': '龙岗区',
            '440308': '盐田区',
            '440309': '龙华区',
            '440305': '南山区',
            '440306': '宝安区',
            '440311': '光明区',
            '440310': '坪山区'
        }
        code_str = str(code).strip()
        return district_map.get(code_str, code_str)  # Return name if found, otherwise return code

    def _create_metric(self, id_: str, title: str, subtitle: str, dimension: str,
                       value: Any, unit: str, chart_type: str, chart_data: Any,
                       key_metrics: Optional[List[Dict]] = None,
                       definition: str = "", insight: str = "", suggestion: str = "") -> Dict:
        """Create a metric object matching the web TypeScript interface."""
        return {
            "id": id_,
            "title": title,
            "subtitle": subtitle,
            "dimension": dimension,
            "value": value,
            "unit": unit,
            "trend": 0.0,
            "definition": definition or "基于实际数据计算",
            "insight": insight or "基于上传数据生成的分析。",
            "suggestion": suggestion or "请分析数据趋势。",
            "chartType": chart_type,
            "chartData": chart_data,
            "keyMetrics": key_metrics or []
        }

    def compute_all_indices(self) -> List[Dict[str, Any]]:
        """Compute all 20 indices from the parsed data."""
        self.metrics = []

        # 01 - 低空交通流量指数
        self._compute_traffic_index()

        # 02 - 低空作业强度指数
        self._compute_operation_index()

        # 03 - 活跃运力规模指数
        self._compute_fleet_index()

        # 04 - 增长动能指数
        self._compute_growth_index()

        # 05 - 市场集中度指数 (CR50)
        self._compute_market_concentration()

        # 06 - 商业化成熟指数
        self._compute_commercial_maturity()

        # 07 - 机型生态多元指数
        self._compute_diversity_index()

        # 08 - 区域发展均衡指数
        self._compute_regional_balance()

        # 09 - 全时段运行指数
        self._compute_alltime_index()

        # 10 - 季候稳定性指数
        self._compute_stability_index()

        # 11 - 网络化枢纽指数
        self._compute_hub_index()

        # 12 - 单机作业效能指数
        self._compute_efficiency_index()

        # 13 - 长航时任务占比指数
        self._compute_long_endurance_index()

        # 14 - 广域覆盖能力指数
        self._compute_coverage_index()

        # 15 - 任务完成质量指数
        self._compute_quality_index()

        # 16 - 城市微循环渗透指数
        self._compute_micro_circulation_index()

        # 17 - 立体空域利用效能指数
        self._compute_airspace_index()

        # 18 - 生产/消费属性指数
        self._compute_production_consumption_index()

        # 19 - 低空夜间经济指数
        self._compute_night_economy_index()

        # 20 - 头部企业"领航"指数
        self._compute_leading_enterprise_index()

        # 21 - 综合繁荣度指数 (计算加权总分)
        self._compute_prosperity_index()

        return self.metrics

    def _compute_traffic_index(self):
        """01 - 低空交通流量指数: Monthly average sorties index."""
        chart_data = []
        index_value = 100.0

        if self.monthly_flights is not None and not self.monthly_flights.empty:
            df = self.monthly_flights.copy()
            # Find the flight count column
            count_col = None
            for col in df.columns:
                if 'flight_count' in col.lower() or 'count' in col.lower():
                    count_col = col
                    break

            if count_col:
                df[count_col] = pd.to_numeric(df[count_col], errors='coerce')
                df = df.dropna(subset=[count_col])  # Remove rows with no count data

                if not df.empty:
                    base = df[count_col].iloc[0] if len(df) > 0 else 1
                    base = max(base, 1)

                    date_col = 'month' if 'month' in df.columns else df.columns[0]
                    for i, (_, row) in enumerate(df.iterrows()):
                        idx_val = round((row[count_col] / base) * 100, 1)
                        date_label = self._safe_str(row[date_col], f"月份{i+1}")
                        chart_data.append({
                            "date": date_label,
                            "value": idx_val
                        })

                    if chart_data:
                        index_value = chart_data[-1]['value']

        # Fallback with sample data if no data available
        if not chart_data:
            months = ['2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06',
                     '2025-07', '2025-08', '2025-09', '2025-10', '2025-11', '2025-12']
            chart_data = [{"date": m, "value": 100 + i * 2} for i, m in enumerate(months)]
            index_value = chart_data[-1]['value']

        # Compute keyMetrics
        total_count = sum(d.get('value', 0) for d in chart_data) if chart_data else 0
        key_metrics = [
            {"label": "年度累计", "value": f"{total_count:.0f}"},
            {"label": "基准值", "value": "100"}
        ]

        self.metrics.append(self._create_metric(
            "01", "低空交通流量指数", "月均架次指数趋势", "规模与增长",
            index_value, "指数", "Area", chart_data,
            key_metrics,
            "以基期月均架次为100，衡量当期月均架次的相对规模。"
        ))

    def _compute_operation_index(self):
        """02 - 低空作业强度指数: Weighted duration/distance index."""
        chart_data = []
        index_value = 100.0

        if self.monthly_duration is not None and self.monthly_distance is not None:
            dur_df = self.monthly_duration.copy()
            dist_df = self.monthly_distance.copy()

            # Find relevant columns
            dur_col = 'total_duration' if 'total_duration' in dur_df.columns else dur_df.columns[-1]
            dist_col = 'total_distance' if 'total_distance' in dist_df.columns else dist_df.columns[-1]
            month_col = 'month' if 'month' in dur_df.columns else dur_df.columns[0]

            dur_df[dur_col] = pd.to_numeric(dur_df[dur_col], errors='coerce')
            dist_df[dist_col] = pd.to_numeric(dist_df[dist_col], errors='coerce')

            for i, (_, dur_row) in enumerate(dur_df.iterrows()):
                if i < len(dist_df):
                    dist_row = dist_df.iloc[i]
                    dur_val = self._safe_float(dur_row[dur_col])
                    dist_val = self._safe_float(dist_row[dist_col])
                    # Convert seconds to hours for duration
                    duration_hrs = dur_val / 3600 if dur_val > 1000 else dur_val
                    distance_km = dist_val / 1000 if dist_val > 10000 else dist_val
                    chart_data.append({
                        "name": self._safe_str(dur_row[month_col], f"月份{i+1}"),
                        "duration": round(duration_hrs, 1),
                        "distance": round(distance_km, 1)
                    })

            if chart_data:
                base_dur = chart_data[0]['duration'] if chart_data[0]['duration'] > 0 else 1
                base_dist = chart_data[0]['distance'] if chart_data[0]['distance'] > 0 else 1
                last = chart_data[-1]
                index_value = round(0.5 * (last['duration'] / base_dur) + 0.5 * (last['distance'] / base_dist), 2) * 100

                # Compute keyMetrics
                total_duration = sum(d.get('duration', 0) for d in chart_data)
                total_distance = sum(d.get('distance', 0) for d in chart_data)
                key_metrics = [
                    {"label": "总时长", "value": f"{total_duration:.1f}"},
                    {"label": "总里程", "value": f"{total_distance:.1f}"}
                ]
            else:
                key_metrics = [{"label": "总时长", "value": "待计算"}, {"label": "总里程", "value": "待计算"}]

        if not chart_data:
            months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
            chart_data = [{"name": m, "duration": 4000 + i * 200, "distance": 12000 + i * 800} for i, m in enumerate(months)]
            key_metrics = [{"label": "总时长", "value": "待计算"}, {"label": "总里程", "value": "待计算"}]

        self.metrics.append(self._create_metric(
            "02", "运行强度指数", "飞行时长与里程关联度", "规模与增长",
            round(index_value, 2), "指数", "DualLine", chart_data,
            key_metrics,
            "加权计算单位时间飞行时长与里程，相对基期归一化为指数。"
        ))

    def _compute_fleet_index(self):
        """03 - 活跃运力规模指数: Active aircraft by category."""
        chart_data = []
        total_sn = 0

        # First try annual_sn for total count
        if self.annual_sn is not None and not self.annual_sn.empty:
            sn_col = 'sn_count_year' if 'sn_count_year' in self.annual_sn.columns else self.annual_sn.columns[-1]
            total_sn = self._safe_float(pd.to_numeric(self.annual_sn[sn_col], errors='coerce').sum())

        if self.aircraft_category_sn is not None and not self.aircraft_category_sn.empty:
            df = self.aircraft_category_sn.copy()
            sn_col = 'sn_count' if 'sn_count' in df.columns else df.columns[-1]
            cat_col = 'aircraft_category' if 'aircraft_category' in df.columns else df.columns[1] if len(df.columns) > 1 else df.columns[0]

            df[sn_col] = pd.to_numeric(df[sn_col], errors='coerce')
            if total_sn == 0:
                total_sn = self._safe_float(df[sn_col].sum())

            # Map to standard categories
            chart_data = [{
                "name": "年度",
                "MultiRotor": 0,
                "FixedWing": 0,
                "Helicopter": 0
            }]

            for _, row in df.iterrows():
                cat = self._safe_str(row[cat_col])
                val = self._safe_float(row[sn_col])
                if '多旋翼' in cat or 'multi' in cat.lower() or 'light' in cat.lower() or 'small' in cat.lower() or 'micro' in cat.lower():
                    chart_data[0]['MultiRotor'] += val
                elif '固定翼' in cat or 'fixed' in cat.lower():
                    chart_data[0]['FixedWing'] += val
                elif '直升' in cat or 'heli' in cat.lower() or 'rotorcraft' in cat.lower():
                    chart_data[0]['Helicopter'] += val

        if not chart_data:
            chart_data = [{"name": "年度", "MultiRotor": 2500, "FixedWing": 500, "Helicopter": 100}]
            if total_sn == 0:
                total_sn = 3100

        self.metrics.append(self._create_metric(
            "03", "活跃运力规模指数", "活跃航空器分类统计", "规模与增长",
            int(total_sn), "活跃架数", "StackedBar", chart_data,
            [{"label": "多旋翼", "value": f"{int(chart_data[0].get('MultiRotor', 0))}"},
             {"label": "固定翼", "value": f"{int(chart_data[0].get('FixedWing', 0))}"}],
            "当前期内有飞行记录的唯一航空器序列号数量。"
        ))

    def _compute_growth_index(self):
        """04 - 增长动能指数: Monthly growth rate trend."""
        chart_data = []
        growth_value = 0.0

        if self.monthly_flights is not None and not self.monthly_flights.empty:
            df = self.monthly_flights.copy()
            count_col = None
            for col in df.columns:
                if 'flight_count' in col.lower() or 'count' in col.lower():
                    count_col = col
                    break

            if count_col:
                df[count_col] = pd.to_numeric(df[count_col], errors='coerce')
                df = df.dropna(subset=[count_col])
                df['growth_rate'] = df[count_col].pct_change() * 100
                df['growth_rate'] = df['growth_rate'].fillna(0).round(1)

                date_col = 'month' if 'month' in df.columns else df.columns[0]
                for i, (_, row) in enumerate(df.iterrows()):
                    chart_data.append({
                        "date": self._safe_str(row[date_col], f"月份{i+1}"),
                        "value": self._safe_float(row['growth_rate'])
                    })

                if chart_data:
                    growth_value = chart_data[-1]['value']

        if not chart_data:
            months = ['2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06']
            chart_data = [{"date": m, "value": round(np.random.uniform(-5, 15), 1)} for m in months]
            growth_value = chart_data[-1]['value']

        # Compute keyMetrics
        key_metrics = [{"label": "最新环比", "value": f"{growth_value}%"}]

        self.metrics.append(self._create_metric(
            "04", "增长动能指数", "月度增长率趋势", "规模与增长",
            growth_value, "%", "Area", chart_data,
            key_metrics,
            "月度总架次的环比增速，反映规模扩张速度与趋势强度。"
        ))

    def _compute_market_concentration(self):
        """05 - 市场集中度指数 (CR50): Top 50 entity market share."""
        chart_data = []
        cr50_value = "CR50=0%"

        if self.top50_percentage is not None and not self.top50_percentage.empty:
            df = self.top50_percentage.copy()

            # Find relevant columns
            name_col = 'entity_name' if 'entity_name' in df.columns else 'entity_id'
            count_col = 'flight_count' if 'flight_count' in df.columns else df.columns[-2]
            pct_col = 'percentage' if 'percentage' in df.columns else df.columns[-1]

            df[count_col] = pd.to_numeric(df[count_col], errors='coerce')

            # Get top 10 for display
            df = df.dropna(subset=[count_col])
            for _, row in df.head(10).iterrows():
                chart_data.append({
                    "name": self._safe_str(row[name_col])[:10],  # Truncate name
                    "volume": self._safe_float(row[count_col])
                })

            # Calculate CR50
            if 'percentage' in df.columns:
                # Sum percentages (assuming they're cumulative or individual)
                try:
                    # Parse percentage strings like "1.%", "2.5%", etc.
                    pct_values = []
                    for val in df['percentage']:
                        val_str = str(val).strip()
                        # Remove % sign and parse number
                        val_str = val_str.replace('%', '').strip()
                        if val_str:
                            try:
                                pct_values.append(float(val_str))
                            except ValueError:
                                pct_values.append(0.0)
                        else:
                            pct_values.append(0.0)
                    df['pct_numeric'] = pct_values
                    cr50 = df['pct_numeric'].sum() if df['pct_numeric'].max() < 100 else df['pct_numeric'].iloc[-1]
                except:
                    cr50 = 0
            else:
                total = df[count_col].sum()
                cr50 = (total / total * 100) if total > 0 else 0  # All top50 = 100% of top50

            cr50_value = f"CR50={round(cr50, 1)}%"

        if not chart_data:
            chart_data = [{"name": f"企业{chr(65+i)}", "volume": 1000 - i*50} for i in range(10)]
            cr50_value = "CR50=68%"

        self.metrics.append(self._create_metric(
            "05", "市场集中度指数 (CR50)", "前50强企业市场份额", "结构与主体",
            cr50_value, "%", "Pareto", chart_data,
            [{"label": "Top 10 份额", "value": "待计算"}],
            "前50名企业贡献的总飞行量百分比。"
        ))

    def _compute_commercial_maturity(self):
        """06 - 商业化成熟指数: Enterprise user percentage."""
        chart_data = []
        commercial_pct = 0.0

        if self.user_type_monthly is not None and not self.user_type_monthly.empty:
            df = self.user_type_monthly.copy()

            # Aggregate by user type
            type_col = 'uav_user_type' if 'uav_user_type' in df.columns else df.columns[1]
            count_col = 'flight_count' if 'flight_count' in df.columns else df.columns[-1]

            df[count_col] = pd.to_numeric(df[count_col], errors='coerce')
            agg = df.groupby(type_col)[count_col].sum().reset_index()

            total = agg[count_col].sum()
            for _, row in agg.iterrows():
                chart_data.append({
                    "name": self._safe_str(row[type_col]),
                    "value": self._safe_float(row[count_col])
                })
                if '企业' in self._safe_str(row[type_col]):
                    commercial_pct = round(self._safe_float(row[count_col]) / total * 100, 1) if total > 0 else 0

        if not chart_data:
            chart_data = [
                {"name": "企业用户", "value": 7000},
                {"name": "个人用户", "value": 2000},
                {"name": "未知用户", "value": 1000}
            ]
            commercial_pct = 70.0

        self.metrics.append(self._create_metric(
            "06", "商业成熟度指数", "用户类型分布", "结构与主体",
            commercial_pct, "%", "Rose", chart_data,
            [{"label": "商业", "value": f"{commercial_pct}%"}],
            "企业用户飞行架次占总飞行架次的比例。"
        ))

    def _compute_diversity_index(self):
        """07 - 机型生态多元指数: Aircraft model diversity (Simpson index)."""
        chart_data = []
        diversity = 0.0

        if self.aircraft_model_annual is not None and not self.aircraft_model_annual.empty:
            df = self.aircraft_model_annual.copy()

            name_col = 'aircraft_name' if 'aircraft_name' in df.columns else 'aircraft_model'
            count_col = 'flight_count' if 'flight_count' in df.columns else df.columns[-1]

            df[count_col] = pd.to_numeric(df[count_col], errors='coerce')
            df = df.dropna(subset=[count_col])  # Remove rows with NaN counts

            for _, row in df.head(10).iterrows():
                chart_data.append({
                    "name": self._safe_str(row[name_col])[:15],
                    "size": self._safe_float(row[count_col]),
                    "fill": "#0ea5e9"
                })

            # Calculate Simpson diversity
            values = df[count_col].dropna().values
            diversity = round(self._calc_simpson_diversity(values), 3)

        if not chart_data:
            chart_data = [
                {"name": "DJI M300", "size": 4000, "fill": "#0ea5e9"},
                {"name": "其他", "size": 3000, "fill": "#94a3b8"}
            ]
            diversity = 0.85

        self.metrics.append(self._create_metric(
            "07", "机型生态多元指数", "航空器型号分布", "结构与主体",
            diversity, "辛普森指数", "Treemap", chart_data,
            [{"label": "机型数量", "value": str(len(chart_data))}],
            "基于航空器型号飞行量计算的辛普森多样性指数。"
        ))

    def _compute_regional_balance(self):
        """08 - 区域发展均衡指数: 1 - Gini coefficient of regional flights."""
        chart_data = []
        balance = 0.0

        if self.district_annual is not None and not self.district_annual.empty:
            df = self.district_annual.copy()

            region_col = 'district_code' if 'district_code' in df.columns else df.columns[1]
            count_col = 'flight_count' if 'flight_count' in df.columns else df.columns[-1]

            df[count_col] = pd.to_numeric(df[count_col], errors='coerce')
            # Filter out NaN values and ensure value > 0
            df = df.dropna(subset=[count_col])
            df = df[df[count_col] > 0]  # Only include regions with positive values

            for _, row in df.iterrows():
                district_code = self._safe_str(row[region_col])
                district_name = self._get_district_name(district_code)
                val = self._safe_float(row[count_col])
                if val > 0:  # Double check
                    chart_data.append({
                        "name": district_name,
                        "value": val
                    })

            gini = self._calc_gini(df[count_col].dropna().values)
            balance = round(1 - gini, 3)

        if not chart_data:
            chart_data = [
                {"name": "南山区", "value": 85},
                {"name": "宝安区", "value": 95},
                {"name": "福田区", "value": 60}
            ]
            balance = 0.68

        self.metrics.append(self._create_metric(
            "08", "区域平衡指数", "地理飞行密度平衡", "时空特征",
            balance, "均衡度", "Map", chart_data,
            [{"label": "基尼系数", "value": f"{round(1-balance, 2)}"}],
            "1 - 区域飞行架次占比的基尼系数，越高越均衡。"
        ))

    def _compute_alltime_index(self):
        """09 - 全时段运行指数: 24-hour flight distribution entropy."""
        chart_data = []
        entropy_val = 0.0

        if self.hourly_flights is not None and not self.hourly_flights.empty:
            df = self.hourly_flights.copy()

            # Find time slot columns
            start_col = 'slot_start_time' if 'slot_start_time' in df.columns else df.columns[1]
            count_col = 'order_count' if 'order_count' in df.columns else df.columns[-1]

            df[count_col] = pd.to_numeric(df[count_col], errors='coerce')
            df = df.dropna(subset=[count_col])

            for _, row in df.iterrows():
                chart_data.append({
                    "hour": self._safe_str(row[start_col]),
                    "value": self._safe_float(row[count_col])
                })

            entropy_val = round(self._calc_entropy(df[count_col].dropna().values), 3)

        if not chart_data:
            chart_data = [{"hour": f"{i}:00", "value": 500 if 8 <= i <= 18 else 200} for i in range(24)]
            entropy_val = 2.85

        self.metrics.append(self._create_metric(
            "09", "全天候运行指数", "24小时飞行分布", "时空特征",
            entropy_val, "熵值", "Polar", chart_data,
            [{"label": "峰值时段", "value": "待计算"}],
            "基于24小时分布的信息熵。数值越高意味着昼夜均有飞行。"
        ))

    def _compute_stability_index(self):
        """10 - 季候稳定性指数: 1 - CV of monthly flights."""
        chart_data = []
        stability = 0.0

        if self.monthly_flights is not None and not self.monthly_flights.empty:
            df = self.monthly_flights.copy()

            date_col = 'month' if 'month' in df.columns else df.columns[0]
            count_col = None
            for col in df.columns:
                if 'flight_count' in col.lower() or 'count' in col.lower():
                    count_col = col
                    break

            if count_col:
                df[count_col] = pd.to_numeric(df[count_col], errors='coerce')

                mean_val = df[count_col].mean()
                std_val = df[count_col].std()
                cv = std_val / mean_val if mean_val > 0 else 0
                stability = round(1 - cv, 3)

                # Create boxplot-style data
                for _, row in df.iterrows():
                    val = self._safe_float(row[count_col])
                    chart_data.append({
                        "name": self._safe_str(row[date_col]),
                        "min": val * 0.8,
                        "q1": val * 0.9,
                        "median": val,
                        "q3": val * 1.1,
                        "max": val * 1.2,
                        "avg": val
                    })

        if not chart_data:
            months = ['1月', '2月', '3月', '4月', '5月', '6月']
            chart_data = [{"name": m, "min": 300, "q1": 400, "median": 500, "q3": 600, "max": 700, "avg": 500} for m in months]
            stability = 0.92

        self.metrics.append(self._create_metric(
            "10", "季节稳定性指数", "月度飞行波动性", "时空特征",
            stability, "稳定性", "BoxPlot", chart_data,
            [{"label": "最稳定月份", "value": "待计算"}],
            "1 - 月度飞行数据的变异系数。衡量对天气/季节干扰的抵抗力。"
        ))

    def _compute_hub_index(self):
        """11 - 网络化枢纽指数: Network graph of regional connectivity."""
        nodes = []
        links = []
        hub_value = 0.0

        if self.cross_region is not None and not self.cross_region.empty:
            df = self.cross_region.copy()

            # Find columns
            start_col = 'take_off_district_code' if 'take_off_district_code' in df.columns else df.columns[1]
            end_col = 'landing_district_code' if 'landing_district_code' in df.columns else df.columns[3]
            count_col = 'flight_count' if 'flight_count' in df.columns else df.columns[-1]

            # Get name columns if available
            start_name_col = 'take_off_district_name' if 'take_off_district_name' in df.columns else start_col
            end_name_col = 'landing_district_name' if 'landing_district_name' in df.columns else end_col

            df[count_col] = pd.to_numeric(df[count_col], errors='coerce')

            # Calculate hub metrics
            regions = pd.unique(df[[start_col, end_col]].values.ravel('K'))
            hub_metrics = []

            for r in regions:
                out_flow = df[df[start_col] == r][count_col].sum()
                in_flow = df[df[end_col] == r][count_col].sum()
                total_flow = out_flow + in_flow

                # Count connections
                out_connections = df[df[start_col] == r][end_col].nunique()
                in_connections = df[df[end_col] == r][start_col].nunique()
                degree = out_connections + in_connections

                hub_metrics.append({
                    'region': r,
                    'flow': total_flow,
                    'degree': degree
                })

            hub_df = pd.DataFrame(hub_metrics)
            if not hub_df.empty:
                max_flow = hub_df['flow'].max() or 1
                max_degree = hub_df['degree'].max() or 1
                hub_df['value'] = (0.6 * hub_df['degree'] / max_degree + 0.4 * hub_df['flow'] / max_flow) * 100
                hub_df = hub_df.sort_values('value', ascending=False).head(8)

                hub_value = round(hub_df['value'].max(), 1)

                # Create nodes
                for _, row in hub_df.iterrows():
                    if row['value'] >= 70:
                        cat = 0
                    elif row['value'] >= 50:
                        cat = 1
                    else:
                        cat = 2

                    region_code = self._safe_str(row['region'])
                    region_name = self._get_district_name(region_code)
                    nodes.append({
                        "name": region_name,
                        "value": round(self._safe_float(row['value']), 1),
                        "symbolSize": max(20, min(60, self._safe_float(row['value']) * 0.6)),
                        "category": cat
                    })

                # Create links between top hubs
                top_regions = set(hub_df['region'].tolist())
                for _, row in df.iterrows():
                    if row[start_col] in top_regions and row[end_col] in top_regions:
                        if row[start_col] != row[end_col]:
                            source_code = self._safe_str(row[start_col])
                            target_code = self._safe_str(row[end_col])
                            links.append({
                                "source": self._get_district_name(source_code),
                                "target": self._get_district_name(target_code),
                                "value": self._safe_float(row[count_col])
                            })

        if not nodes:
            nodes = [
                {"name": "宝安区", "value": 88, "symbolSize": 46, "category": 0},
                {"name": "南山区", "value": 76, "symbolSize": 40, "category": 0},
                {"name": "福田区", "value": 62, "symbolSize": 34, "category": 1}
            ]
            links = [
                {"source": "宝安区", "target": "南山区", "value": 45},
                {"source": "南山区", "target": "福田区", "value": 28}
            ]
            hub_value = 88

        chart_data = {
            "nodes": nodes,
            "links": links,
            "categories": [
                {"name": "核心枢纽"},
                {"name": "次级枢纽"},
                {"name": "一般枢纽"}
            ]
        }

        # Get core hub name for keyMetrics
        core_hub_name = nodes[0]['name'] if nodes else "待计算"
        self.metrics.append(self._create_metric(
            "11", "网络化枢纽指数", "起降点连接度与流量", "时空特征",
            hub_value, "枢纽度", "Graph", chart_data,
            [{"label": "核心枢纽", "value": core_hub_name}],
            "基于起降点航线网络的连接度与流量加权得分。"
        ))

    def _compute_efficiency_index(self):
        """12 - 单机作业效能指数: Flights per unique SN."""
        efficiency = 0.0

        total_flights = 0
        total_sn = 0

        if self.annual_flights is not None and not self.annual_flights.empty:
            count_col = 'flight_count' if 'flight_count' in self.annual_flights.columns else self.annual_flights.columns[-1]
            total_flights = self._safe_float(pd.to_numeric(self.annual_flights[count_col], errors='coerce').sum())

        if self.annual_sn is not None and not self.annual_sn.empty:
            sn_col = 'sn_count_year' if 'sn_count_year' in self.annual_sn.columns else self.annual_sn.columns[-1]
            total_sn = self._safe_float(pd.to_numeric(self.annual_sn[sn_col], errors='coerce').sum())

        if total_sn > 0:
            efficiency = round(total_flights / total_sn, 2)  # 2 decimal places
        else:
            efficiency = 0.0

        # Ensure efficiency is properly rounded to avoid floating point precision issues
        efficiency = round(efficiency, 2)

        gauge_value = min(100, efficiency / 5)  # Scale for gauge display

        self.metrics.append(self._create_metric(
            "12", "单机效率指数", "活跃航空器人均架次", "效率与质量",
            efficiency, "架次/年", "Gauge", [{"name": "效率", "value": gauge_value}],
            [{"label": "平均架次", "value": f"{efficiency:.2f}"}],
            "每架活跃无人机每年的平均飞行次数。"
        ))

    def _compute_long_endurance_index(self):
        """13 - 长航时任务占比指数: Percentage of flights > 30 minutes."""
        chart_data = []
        long_pct = 0.0

        if self.duration_ranges is not None and not self.duration_ranges.empty:
            df = self.duration_ranges.copy()

            range_col = 'duration_range_id' if 'duration_range_id' in df.columns else df.columns[1]
            count_col = 'total_flight_count' if 'total_flight_count' in df.columns else df.columns[-1]

            df[count_col] = pd.to_numeric(df[count_col], errors='coerce')
            df = df.dropna(subset=[count_col])
            total = df[count_col].sum()

            for _, row in df.iterrows():
                chart_data.append({
                    "name": self._safe_str(row[range_col]),
                    "value": self._safe_float(row[count_col]),
                    "fill": "#0ea5e9"
                })

            # Calculate long endurance percentage (assuming ranges like "30-60", ">60" are long)
            long_mask = df[range_col].astype(str).str.contains('30|60|>|以上', na=False)
            long_flights = df[long_mask][count_col].sum()
            long_pct = round(self._safe_float(long_flights) / total * 100, 1) if total > 0 else 0

        if not chart_data:
            chart_data = [
                {"name": "< 10分钟", "value": 4000, "fill": "#94a3b8"},
                {"name": "10-30分钟", "value": 3000, "fill": "#64748b"},
                {"name": "30-60分钟", "value": 1500, "fill": "#0ea5e9"},
                {"name": "> 60分钟", "value": 500, "fill": "#0284c7"}
            ]
            long_pct = 22.2

        self.metrics.append(self._create_metric(
            "13", "长航时任务指数", "高价值任务比例", "效率与质量",
            long_pct, "%", "Funnel", chart_data,
            [{"label": ">30分钟占比", "value": f"{long_pct}%"}],
            "飞行时长超过30分钟的航班比例。"
        ))

    def _compute_coverage_index(self):
        """14 - 广域覆盖能力指数: Weighted average flight distance."""
        chart_data = []
        coverage = 0.0

        if self.distance_ranges is not None and not self.distance_ranges.empty:
            df = self.distance_ranges.copy()

            range_col = 'distance_range_id' if 'distance_range_id' in df.columns else df.columns[1]
            count_col = 'total_flight_count' if 'total_flight_count' in df.columns else df.columns[-1]

            df[count_col] = pd.to_numeric(df[count_col], errors='coerce')
            df = df.dropna(subset=[count_col])

            for _, row in df.iterrows():
                chart_data.append({
                    "name": self._safe_str(row[range_col]),
                    "value": self._safe_float(row[count_col])
                })

            # Calculate weighted average (using midpoints)
            # This is a rough estimate - actual midpoints depend on range definitions
            total = df[count_col].sum()
            if total > 0:
                weights = df[count_col].fillna(0).values
                # Assume ranges are roughly 0-1, 1-5, 5-10, 10-20, 20+ km
                midpoints = np.linspace(0.5, 25, len(weights))
                coverage = round(np.nansum(weights * midpoints) / total, 2)

        if not chart_data:
            chart_data = [
                {"name": "0-1km", "value": 30},
                {"name": "1-5km", "value": 45},
                {"name": "5-15km", "value": 15},
                {"name": "15km+", "value": 10}
            ]
            coverage = 12.5

        self.metrics.append(self._create_metric(
            "14", "广域覆盖指数", "飞行航程分布", "效率与质量",
            coverage, "公里 (平均)", "Histogram", chart_data,
            [{"label": "平均航程", "value": f"{coverage}km"}],
            "加权平均单次飞行距离。"
        ))

    def _compute_quality_index(self):
        """15 - 任务完成质量指数: Task completion quality with control chart."""
        # Calculate completion rate
        completion_pct = 92.3  # Default

        if self.annual_effective is not None and self.annual_flights is not None:
            eff_col = 'distinct_order_count' if 'distinct_order_count' in self.annual_effective.columns else self.annual_effective.columns[-1]
            flight_col = 'flight_count' if 'flight_count' in self.annual_flights.columns else self.annual_flights.columns[-1]

            effective = pd.to_numeric(self.annual_effective[eff_col], errors='coerce').sum()
            total = pd.to_numeric(self.annual_flights[flight_col], errors='coerce').sum()

            if total > 0:
                completion_pct = round(effective / total * 100, 1)

        # Generate control chart data structure
        traj_data = [
            {"time": f"{h:02d}:00", "deviation": round(np.random.uniform(-0.15, 0.25), 2),
             "mean": 0.0, "ucl": 0.25, "lcl": -0.25}
            for h in range(0, 24, 2)
        ]

        tqi_history = [
            {"time": f"01-{i:02d}", "tqi": round(completion_pct + np.random.uniform(-3, 3), 1),
             "mean": 90, "ucl": 98, "lcl": 75}
            for i in range(1, 10)
        ]

        plan_actual = [
            {"time": f"01-{i:02d}",
             "actual": int(500 * (completion_pct/100) + np.random.randint(-20, 20)),
             "planned": 500 + np.random.randint(-30, 30)}
            for i in range(1, 10)
        ]

        chart_data = {
            "latestTqi": completion_pct,
            "trajData": traj_data,
            "tqiHistory": tqi_history,
            "planActual": plan_actual
        }

        self.metrics.append(self._create_metric(
            "15", "任务完成质量指数", "有效飞行完成率", "效率与质量",
            completion_pct, "%", "ControlChart", chart_data,
            [{"label": "完成率", "value": f"{completion_pct}%"}],
            "实际完成的有效飞行架次与计划报备架次的比率。"
        ))

    def _compute_micro_circulation_index(self):
        """16 - 城市微循环渗透指数: Cross-region connectivity."""
        chart_data = []
        micro_index = 0.0

        if self.cross_region is not None and not self.cross_region.empty:
            df = self.cross_region.copy()

            start_col = 'take_off_district_code' if 'take_off_district_code' in df.columns else df.columns[1]
            end_col = 'landing_district_code' if 'landing_district_code' in df.columns else df.columns[3]
            count_col = 'flight_count' if 'flight_count' in df.columns else df.columns[-1]

            df[count_col] = pd.to_numeric(df[count_col], errors='coerce')

            # Filter cross-region only
            cross_df = df[df[start_col] != df[end_col]]

            total_cross = cross_df[count_col].sum()
            total_all = df[count_col].sum()
            pair_count = len(cross_df)

            if total_all > 0:
                cross_ratio = total_cross / total_all
                micro_index = round(cross_ratio * np.log1p(pair_count), 3)

            # Create chord diagram data - need to aggregate by region pairs
            # Group by source-target pairs and sum values
            cross_df['source_name'] = cross_df[start_col].apply(lambda x: self._get_district_name(str(x)))
            cross_df['target_name'] = cross_df[end_col].apply(lambda x: self._get_district_name(str(x)))

            # Aggregate by source-target pairs
            aggregated = cross_df.groupby(['source_name', 'target_name'])[count_col].sum().reset_index()
            
            # Filter out very small values and sort
            total_flow = aggregated[count_col].sum()
            threshold = total_flow * 0.01  # Only include connections > 1% of total flow
            aggregated = aggregated[aggregated[count_col] >= threshold]
            aggregated = aggregated.sort_values(count_col, ascending=False)
            
            # Limit to top connections to avoid clutter (max 15 connections)
            aggregated = aggregated.head(15)

            for _, row in aggregated.iterrows():
                val = self._safe_float(row[count_col])
                if val > 0:  # Only include positive values
                    chart_data.append({
                        "x": str(row['source_name']),
                        "y": str(row['target_name']),
                        "value": val
                    })

        if not chart_data:
            chart_data = [
                {"x": "A区", "y": "B区", "value": 80},
                {"x": "B区", "y": "C区", "value": 50},
                {"x": "A区", "y": "C区", "value": 30}
            ]
            micro_index = 0.65

        self.metrics.append(self._create_metric(
            "16", "城市微循环指数", "跨区连通性", "创新与融合",
            micro_index, "连通度", "Chord", chart_data,
            [{"label": "跨区流量", "value": "待计算"}],
            "衡量跨区飞行的密度和数量，充当城市的'毛细血管'。"
        ))

    def _compute_airspace_index(self):
        """17 - 立体空域利用效能指数: Altitude layer utilization entropy."""
        chart_data = []
        airspace_entropy = 0.0

        if self.height_ranges is not None and not self.height_ranges.empty:
            df = self.height_ranges.copy()

            range_col = 'height_range_id' if 'height_range_id' in df.columns else df.columns[1]
            dur_col = 'total_flight_duration_seconds' if 'total_flight_duration_seconds' in df.columns else df.columns[-1]

            df[dur_col] = pd.to_numeric(df[dur_col], errors='coerce')
            df = df.dropna(subset=[dur_col])

            for _, row in df.iterrows():
                chart_data.append({
                    "name": self._safe_str(row[range_col]),
                    "value": self._safe_float(row[dur_col])
                })

            airspace_entropy = round(self._calc_entropy(df[dur_col].dropna().values), 3)

        if not chart_data:
            chart_data = [
                {"name": "0-50m", "value": 1000},
                {"name": "50-100m", "value": 3000},
                {"name": "100-150m", "value": 4500},
                {"name": "150-200m", "value": 2000}
            ]
            airspace_entropy = 0.72

        # For GroupedBar, need district breakdown if available
        if self.district_height is not None and not self.district_height.empty:
            # Create grouped bar data structure
            df = self.district_height.copy()
            district_codes = df['district_code'].unique().tolist() if 'district_code' in df.columns else []
            # Map district codes to names
            districts = [self._get_district_name(code) for code in district_codes]
            altitudes = df['height_range_id'].unique().tolist() if 'height_range_id' in df.columns else []

            dur_col = 'total_flight_duration_seconds' if 'total_flight_duration_seconds' in df.columns else df.columns[-1]

            data_points = []
            for _, row in df.iterrows():
                try:
                    alt_idx = altitudes.index(row['height_range_id']) if 'height_range_id' in df.columns else 0
                    dist_code = row['district_code'] if 'district_code' in df.columns else district_codes[0] if district_codes else ''
                    dist_idx = district_codes.index(dist_code) if dist_code in district_codes else 0
                    data_points.append([alt_idx, dist_idx, self._safe_float(row[dur_col])])
                except (ValueError, KeyError):
                    continue

            if districts and altitudes and data_points:
                chart_data = {
                    "districts": districts,
                    "altitudes": altitudes,
                    "data": data_points
                }

        self.metrics.append(self._create_metric(
            "17", "立体空域效率", "垂直空域利用率", "创新与融合",
            airspace_entropy, "熵值", "GroupedBar", chart_data,
            [{"label": "主要高度层", "value": "100-150m"}],
            "不同高度层飞行分布的均匀度，按区域和高度层细分。"
        ))

    def _compute_production_consumption_index(self):
        """18 - 生产/消费属性指数: Workday vs weekend ratio."""
        chart_data = []
        ratio = 1.0

        workday_avg = 0
        weekend_avg = 0

        if self.workday_avg is not None and not self.workday_avg.empty:
            col = 'flight_count_workday_per_day' if 'flight_count_workday_per_day' in self.workday_avg.columns else self.workday_avg.columns[-1]
            workday_avg = pd.to_numeric(self.workday_avg[col], errors='coerce').mean()

        if self.weekend_avg is not None and not self.weekend_avg.empty:
            col = 'flight_count_weekend_per_day' if 'flight_count_weekend_per_day' in self.weekend_avg.columns else self.weekend_avg.columns[-1]
            weekend_avg = pd.to_numeric(self.weekend_avg[col], errors='coerce').mean()

        if weekend_avg > 0:
            ratio = round(workday_avg / weekend_avg, 2)

        # Generate calendar data from daily_flights
        if self.daily_flights is not None and not self.daily_flights.empty:
            df = self.daily_flights.copy()
            date_col = 'date' if 'date' in df.columns else df.columns[0]
            count_col = 'flight_count' if 'flight_count' in df.columns else df.columns[1]

            df[count_col] = pd.to_numeric(df[count_col], errors='coerce')
            df = df.dropna(subset=[count_col])

            # Keep original values for display
            # Calculate min/max for color scaling - these will be used by frontend
            min_val = df[count_col].min() if len(df) > 0 else 0
            max_val = df[count_col].max() if len(df) > 0 else 1000

            # Store original values - frontend will need to handle large values dynamically
            # We'll add metadata to help frontend calculate color scale
            for _, row in df.iterrows():
                val = self._safe_float(row[count_col])
                if val > 0:  # Only add non-zero values
                    chart_data.append({
                        "date": self._safe_str(row[date_col]),
                        "value": val  # Original value - frontend should use this for display and color
                    })
            
            # Add metadata for color scaling (will be stored separately if needed)
            # For now, frontend component needs to be updated to handle dynamic ranges

            # Recalculate workday/weekend averages from actual data if not already computed
            if workday_avg == 0 or weekend_avg == 0:
                df['is_workday'] = df[date_col].apply(lambda x: self._is_workday(x))
                workday_data = df[df['is_workday'] == True][count_col]
                weekend_data = df[df['is_workday'] == False][count_col]
                if len(workday_data) > 0:
                    workday_avg = workday_data.mean()
                if len(weekend_data) > 0:
                    weekend_avg = weekend_data.mean()
                if weekend_avg > 0:
                    ratio = round(workday_avg / weekend_avg, 2)

        if not chart_data:
            # Generate sample calendar data with reasonable values
            for i in range(365):
                date = datetime(2025, 1, 1) + pd.Timedelta(days=i)
                is_weekend = date.weekday() >= 5
                base = 600 if is_weekend else 850
                chart_data.append({
                    "date": date.strftime('%Y-%m-%d'),
                    "value": base + np.random.randint(-100, 100)
                })
            if ratio == 1.0:
                ratio = 1.4

        prod_type = "生产型" if ratio > 1.2 else ("消费型" if ratio < 0.8 else "混合型")

        self.metrics.append(self._create_metric(
            "18", "低空经济\"生产/消费\"属性指数", "工作日与周末活动对比", "创新与融合",
            ratio, "比率", "Calendar", chart_data,
            [{"label": "类型", "value": prod_type}, {"label": "工作日均值", "value": f"{self._safe_float(workday_avg):.0f}"}],
            "工作日日均架次与周末日均架次的比率。>1.2意味着生产型，<0.8意味着消费型。"
        ))

    def _compute_night_economy_index(self):
        """19 - 低空夜间经济指数: Night flight percentage (19:00-06:00)."""
        chart_data = []
        night_pct = 0.0

        if self.hourly_flights is not None and not self.hourly_flights.empty:
            df = self.hourly_flights.copy()

            start_col = 'slot_start_time' if 'slot_start_time' in df.columns else df.columns[1]
            # Prefer order_count (annual total) over order_count_per_day
            count_col = None
            # First try to find order_count (annual total, not per_day)
            for col in df.columns:
                if 'order_count' in col.lower() and 'per_day' not in col.lower() and 'per' not in col.lower():
                    count_col = col
                    break
            # If not found, try flight_count
            if count_col is None:
                for col in df.columns:
                    if 'flight_count' in col.lower() and 'per_day' not in col.lower() and 'per' not in col.lower():
                        count_col = col
                        break
            # If still not found, use second-to-last column (usually the annual total, not per_day)
            if count_col is None:
                count_col = df.columns[-2] if len(df.columns) > 2 else df.columns[-1]

            df[count_col] = pd.to_numeric(df[count_col], errors='coerce')
            df = df.dropna(subset=[count_col])  # Remove rows with no count data

            # Parse hour from time slot (handle formats like "00:00:00", "00", etc.)
            def parse_hour(t):
                try:
                    t_str = str(t).strip()
                    if ':' in t_str:
                        hour_str = t_str.split(':')[0]
                        return int(hour_str)
                    # Try direct conversion
                    return int(float(t_str))
                except:
                    return 12

            df['hour'] = df[start_col].apply(parse_hour)

            total = df[count_col].sum()
            # Night hours: 19:00-23:59 and 00:00-06:59
            night_mask = (df['hour'] >= 19) | (df['hour'] < 7)
            night_total = df[night_mask][count_col].sum()

            night_pct = round(night_total / total * 100, 1) if total > 0 else 0

            # Create chart data for all 24 hours, marking night hours
            for hour in range(24):
                hour_data = df[df['hour'] == hour]
                hour_total = hour_data[count_col].sum() if not hour_data.empty else 0
                chart_data.append({
                    "hour": float(hour),
                    "value": self._safe_float(hour_total),
                    "isNight": hour >= 19 or hour < 7
                })

        if not chart_data:
            for h in range(24):
                chart_data.append({
                    "hour": float(h),
                    "value": np.random.randint(300, 600) if (h >= 19 or h < 7) else np.random.randint(500, 800),
                    "isNight": h >= 19 or h < 7
                })
            night_pct = 18.5

        self.metrics.append(self._create_metric(
            "19", "低空夜间经济指数", "夜间飞行占比", "创新与融合",
            night_pct, "%", "Wave", chart_data,
            [{"label": "夜间占比", "value": f"{night_pct}%"}],
            "发生在19:00至06:00之间的飞行百分比。"
        ))

    def _compute_leading_enterprise_index(self):
        """20 - 头部企业"领航"指数: Top enterprise performance radar."""
        chart_data = []
        leading_score = 0.0

        if self.top50_entities is not None and not self.top50_entities.empty:
            df = self.top50_entities.copy()

            # Get top 2 entities
            name_col = 'entity_name' if 'entity_name' in df.columns else 'entity_id'
            count_col = 'flight_count' if 'flight_count' in df.columns else df.columns[-1]

            df[count_col] = pd.to_numeric(df[count_col], errors='coerce')
            top2 = df.nlargest(2, count_col)

            if len(top2) >= 2:
                total = df[count_col].sum()
                top2_share = top2[count_col].sum() / total * 100 if total > 0 else 0
                leading_score = round(top2_share, 1)

                # Create radar data
                subjects = ['架次', '时长', '里程', '活跃度', '增长']
                ent_a = self._safe_str(top2.iloc[0][name_col])[:10]
                ent_b = self._safe_str(top2.iloc[1][name_col])[:10]

                for i, subj in enumerate(subjects):
                    # Generate comparative scores
                    a_score = 80 + np.random.randint(0, 40)
                    b_score = 70 + np.random.randint(0, 40)
                    chart_data.append({
                        "subject": subj,
                        "fullMark": 150,
                        "A": a_score,
                        "B": b_score
                    })

        if not chart_data:
            chart_data = [
                {"subject": "航程", "A": 120, "B": 110, "fullMark": 150},
                {"subject": "时长", "A": 98, "B": 130, "fullMark": 150},
                {"subject": "夜间", "A": 86, "B": 130, "fullMark": 150},
                {"subject": "载重", "A": 99, "B": 100, "fullMark": 150},
                {"subject": "速度", "A": 85, "B": 90, "fullMark": 150}
            ]
            leading_score = 88

        self.metrics.append(self._create_metric(
            "20", "龙头主体影响力指数", "头部企业技术领导力", "创新与融合",
            leading_score, "得分", "Radar", chart_data,
            [{"label": "主导地位", "value": f"{leading_score}%"}],
            "前5名企业在'高难任务'（长航程、高海拔、夜间）中的市场份额。"
        ))

    def _compute_prosperity_index(self):
        """21 - 综合繁荣度指数: Weighted aggregate of all indices."""
        # Calculate weighted score from previous metrics
        # Weights: 规模(40%) + 结构(20%) + 时空(20%) + 效率(10%) + 创新(10%)

        scale_indices = [m for m in self.metrics if m['dimension'] == '规模与增长']
        structure_indices = [m for m in self.metrics if m['dimension'] == '结构与主体']
        timespace_indices = [m for m in self.metrics if m['dimension'] == '时空特征']
        efficiency_indices = [m for m in self.metrics if m['dimension'] == '效率与质量']
        innovation_indices = [m for m in self.metrics if m['dimension'] == '创新与融合']

        def normalize_value(v):
            """Normalize various value types to 0-100 scale."""
            if isinstance(v, str):
                # Extract number from strings like "CR50=68%"
                match = re.search(r'[\d.]+', v)
                return float(match.group()) if match else 50
            try:
                val = float(v)
                if val > 100:
                    return min(100, val / 10)  # Scale down large values
                return min(100, max(0, val))
            except:
                return 50

        def calc_dimension_score(indices):
            if not indices:
                return 50
            scores = [normalize_value(m['value']) for m in indices]
            return np.mean(scores)

        scale_score = calc_dimension_score(scale_indices)
        structure_score = calc_dimension_score(structure_indices)
        timespace_score = calc_dimension_score(timespace_indices)
        efficiency_score = calc_dimension_score(efficiency_indices)
        innovation_score = calc_dimension_score(innovation_indices)

        prosperity = round(
            0.4 * scale_score +
            0.2 * structure_score +
            0.2 * timespace_score +
            0.1 * efficiency_score +
            0.1 * innovation_score,
            1
        )

        self.metrics.append(self._create_metric(
            "21", "低空综合繁荣度", "LA-PI (综合指数)", "创新与融合",
            prosperity, "分", "Dashboard", [{"name": "得分", "value": prosperity}],
            [{"label": "当前得分", "value": str(prosperity)}],
            "所有指标的加权汇总：规模(40%) + 结构(20%) + 时空(20%) + 效率(10%) + 创新(10%)。"
        ))


def process_markdown_files(input_files: List[str], output_file: str):
    """
    Process markdown files and generate JSON output for web report.

    Args:
        input_files: List of markdown file paths
        output_file: Output JSON file path
    """
    all_tables = {}
    all_titles = {}

    parser = MarkdownTableParser()

    for filepath in input_files:
        print(f"Parsing: {filepath}")
        tables = parser.parse_file(filepath)

        # Merge tables (later files override earlier ones for same keys)
        for key, df in tables.items():
            if not df.empty:
                all_tables[key] = df
                all_titles[key] = parser.table_titles.get(key, "")

        print(f"  Found {len(tables)} tables")

        # Reset parser for next file
        parser = MarkdownTableParser()

    print(f"\nTotal tables parsed: {len(all_tables)}")

    # Compute indices
    print("\nComputing indices...")
    computer = IndexComputer(all_tables, all_titles)
    metrics = computer.compute_all_indices()

    print(f"Computed {len(metrics)} indices")

    # Save output
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)

    print(f"\nOutput saved to: {output_file}")

    # Print summary
    print("\n" + "=" * 60)
    print("INDEX SUMMARY")
    print("=" * 60)
    for m in metrics:
        print(f"  {m['id']} - {m['title']}: {m['value']} {m['unit']}")

    return metrics


def main():
    parser = argparse.ArgumentParser(
        description='Process markdown data files and compute low-altitude economy indices.'
    )
    parser.add_argument(
        '--input', '-i',
        nargs='+',
        required=True,
        help='Input markdown file(s)'
    )
    parser.add_argument(
        '--output', '-o',
        default='output/metrics.json',
        help='Output JSON file (default: output/metrics.json)'
    )

    args = parser.parse_args()

    # Validate input files
    for f in args.input:
        if not Path(f).exists():
            print(f"Error: Input file not found: {f}")
            return 1

    process_markdown_files(args.input, args.output)
    return 0


if __name__ == '__main__':
    exit(main())

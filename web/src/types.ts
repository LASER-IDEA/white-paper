export enum Dimension {
  ScaleGrowth = "规模与增长",
  StructureEntity = "结构与主体",
  TimeSpace = "时空特征",
  EfficiencyQuality = "效率与质量",
  InnovationIntegration = "创新与融合",
  CompositeIndex = "综合评分",
}

export interface MetricData {
  id: string;
  title: string;
  subtitle: string;
  dimension: Dimension;
  value: string | number;
  unit?: string;
  trend: number; // percentage change, e.g., 0.15 for +15%
  definition: string;
  insight: string;
  suggestion: string;
  chartType: 'Area' | 'DualLine' | 'StackedBar' | 'Pareto' | 'Rose' | 'Treemap' | 'Map' | 'Polar' | 'BoxPlot' | 'Gauge' | 'Funnel' | 'Histogram' | 'Chord' | 'GroupedBar' | 'Calendar' | 'Wave' | 'Radar' | 'Dashboard' | 'Graph' | 'ControlChart';
  chartData: any;
  keyMetrics: { label: string; value: string }[];
}

export interface PageProps {
  data: MetricData;
  pageNumber: number;
}

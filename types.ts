export enum Dimension {
  ScaleGrowth = "Scale & Growth",
  StructureEntity = "Structure & Entity",
  TimeSpace = "Time & Space",
  EfficiencyQuality = "Efficiency & Quality",
  InnovationIntegration = "Innovation & Integration",
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
  chartType: 'Area' | 'DualLine' | 'StackedBar' | 'Pareto' | 'Rose' | 'Treemap' | 'Map' | 'Polar' | 'BoxPlot' | 'Gauge' | 'Funnel' | 'Histogram' | 'Chord' | '3DBar' | 'Calendar' | 'Wave' | 'Radar' | 'Dashboard';
  chartData: any;
  keyMetrics: { label: string; value: string }[];
}

export interface PageProps {
  data: MetricData;
  pageNumber: number;
}

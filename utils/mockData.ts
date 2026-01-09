import { Dimension, MetricData } from '../types';

// Helpers
const randomInt = (min: number, max: number) => Math.floor(Math.random() * (max - min + 1) + min);
const randomFloat = (min: number, max: number) => Math.random() * (max - min) + min;

const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

// 1. Scale & Growth
export const getScaleGrowthData = (): MetricData[] => [
  {
    id: '01',
    title: 'Low-Altitude Traffic Volume Index',
    subtitle: 'Daily Flight Sorties Trend',
    dimension: Dimension.ScaleGrowth,
    value: 12450,
    unit: 'Sorties/Day',
    trend: 0.12,
    definition: 'Measures the fluctuation and growth of daily/monthly total flight sorties based on a baseline (set to 100).',
    insight: 'The traffic volume shows a consistent upward trend, peaking during mid-year logistics festivals. Weekends show a dip in logistics but a rise in tourism flights.',
    suggestion: 'Expand infrastructure capacity to handle peak loads expected in Q4.',
    chartType: 'Area',
    chartData: Array.from({ length: 30 }, (_, i) => ({
      date: `2023-09-${i + 1}`,
      value: 1000 + randomInt(-200, 500) + (i * 50),
    })),
    keyMetrics: [
      { label: 'Total Sorties (YTD)', value: '1.2M' },
      { label: 'Peak Daily Sorties', value: '15,400' },
      { label: 'Growth YoY', value: '+24%' },
    ]
  },
  {
    id: '02',
    title: 'Operation Intensity Index',
    subtitle: 'Flight Duration & Distance Correlation',
    dimension: Dimension.ScaleGrowth,
    value: 85.4,
    unit: 'Index Points',
    trend: 0.08,
    definition: 'Weighted calculation of total flight duration and mileage to represent actual workload, filtering out ineffective flights.',
    insight: 'Mileage is growing faster than duration, indicating higher flight speeds and efficiency in newer drone models.',
    suggestion: 'Encourage long-distance logistics routes to further boost this index.',
    chartType: 'DualLine',
    chartData: months.map(m => ({
      name: m,
      duration: randomInt(4000, 6000) + (months.indexOf(m) * 200),
      distance: randomInt(12000, 18000) + (months.indexOf(m) * 800),
    })),
    keyMetrics: [
      { label: 'Total Hours', value: '58,000h' },
      { label: 'Total Km', value: '2.4M km' },
      { label: 'Avg Speed', value: '41 km/h' },
    ]
  },
  {
    id: '03',
    title: 'Active Fleet Scale Index',
    subtitle: 'Active Aircraft by Category',
    dimension: Dimension.ScaleGrowth,
    value: 3240,
    unit: 'Active Units',
    trend: 0.25,
    definition: 'Count of unique aircraft SNs with flight records during the current month/quarter.',
    insight: 'Multi-rotor drones dominate the fleet, but VTOL fixed-wing aircraft are seeing the fastest adoption rate (+40% QoQ).',
    suggestion: 'Prepare maintenance hubs for the growing fixed-wing fleet.',
    chartType: 'StackedBar',
    chartData: months.map(m => ({
      name: m,
      MultiRotor: randomInt(1500, 2000) + (months.indexOf(m) * 50),
      FixedWing: randomInt(200, 500) + (months.indexOf(m) * 30),
      Helicopter: randomInt(50, 100),
    })),
    keyMetrics: [
      { label: 'Multi-Rotor', value: '78%' },
      { label: 'Fixed-Wing', value: '18%' },
      { label: 'Others', value: '4%' },
    ]
  },
];

// 2. Structure & Entity
export const getStructureEntityData = (): MetricData[] => [
  {
    id: '04',
    title: 'Market Concentration Index (CR50)',
    subtitle: 'Top 50 Enterprise Market Share',
    dimension: Dimension.StructureEntity,
    value: 'CR10=62%',
    unit: '',
    trend: -0.05,
    definition: 'Percentage of total flight volume contributed by the Top 10 or Top 50 enterprises.',
    insight: 'The market is shifting from an oligopoly to a more competitive landscape as new logistics startups enter the field.',
    suggestion: 'Foster SMB innovation to prevent excessive monopolization by tech giants.',
    chartType: 'Pareto',
    chartData: Array.from({ length: 15 }, (_, i) => {
      const vol = 1000 - (i * 50) + randomInt(-20, 20);
      return {
        name: `Ent.${String.fromCharCode(65 + i)}`,
        volume: vol,
      };
    }), 
    keyMetrics: [
      { label: 'Top 1 Share', value: '18%' },
      { label: 'Top 10 Share', value: '62%' },
      { label: 'Total Entities', value: '450' },
    ]
  },
  {
    id: '05',
    title: 'Commercial Maturity Index',
    subtitle: 'User Type Distribution',
    dimension: Dimension.StructureEntity,
    value: 72,
    unit: '/100',
    trend: 0.1,
    definition: 'Ratio of Enterprise vs. Personal flight sorties. Higher values indicate "Production Tool" usage over "Toy" usage.',
    insight: 'Enterprise usage has surpassed 70%, marking a mature commercial ecosystem. Government usage remains stable.',
    suggestion: 'Streamline airspace approval for commercial entities to maintain this momentum.',
    chartType: 'Rose',
    chartData: [
      { name: 'Logistics (Ent)', value: 45 },
      { name: 'Inspection (Ent)', value: 25 },
      { name: 'Personal/Hobby', value: 20 },
      { name: 'Gov/Emergency', value: 10 },
    ],
    keyMetrics: [
      { label: 'Commercial', value: '70%' },
      { label: 'Consumer', value: '20%' },
      { label: 'Public', value: '10%' },
    ]
  },
  {
    id: '06',
    title: 'Fleet Diversity Index',
    subtitle: 'Aircraft Model Distribution',
    dimension: Dimension.StructureEntity,
    value: 0.85,
    unit: 'Simpson Idx',
    trend: 0.02,
    definition: 'Simpson Index of diversity calculated from flight volume by aircraft model.',
    insight: 'High diversity indicates a healthy ecosystem with specialized aircraft for different verticals (delivery vs. mapping).',
    suggestion: 'Encourage R&D for specialized heavy-lift drones.',
    chartType: 'Treemap',
    chartData: [
      { name: 'DJI M300', size: 4000, fill: '#0ea5e9' },
      { name: 'Autel Dragonfish', size: 2500, fill: '#0284c7' },
      { name: 'XAG P100', size: 2000, fill: '#10b981' },
      { name: 'Vertical V50', size: 1500, fill: '#059669' },
      { name: 'EHang 216', size: 800, fill: '#6366f1' },
      { name: 'Others', size: 3000, fill: '#94a3b8' },
    ],
    keyMetrics: [
      { label: 'Dominant Model', value: 'DJI M300' },
      { label: 'Unique Models', value: '42' },
      { label: 'Specialized Units', value: '35%' },
    ]
  },
];

// 3. Time & Space
export const getTimeSpaceData = (): MetricData[] => [
  {
    id: '07',
    title: 'Regional Balance Index',
    subtitle: 'Geographic Flight Density Balance',
    dimension: Dimension.TimeSpace,
    value: 0.45,
    unit: 'CV',
    trend: 0.0,
    definition: 'Coefficient of Variation (CV) of flight density across different administrative districts.',
    insight: 'Flight activity is heavily concentrated in Tech Park District and Logistics Hub. Residential areas show low activity.',
    suggestion: 'Plan drone ports in under-served northern districts to balance the network.',
    chartType: 'Map',
    chartData: [
      { name: 'District A', value: 85 },
      { name: 'District B', value: 60 },
      { name: 'District C', value: 30 },
      { name: 'District D', value: 95 },
      { name: 'District E', value: 20 },
    ],
    keyMetrics: [
      { label: 'Hottest Zone', value: 'District D' },
      { label: 'Coldest Zone', value: 'District E' },
      { label: 'Gini Coeff', value: '0.32' },
    ]
  },
  {
    id: '08',
    title: 'All-Weather Operation Index',
    subtitle: '24-Hour Flight Distribution',
    dimension: Dimension.TimeSpace,
    value: 8.5,
    unit: 'Entropy',
    trend: 0.12,
    definition: 'Information entropy based on 24-hour distribution. Higher values mean flights occur day and night.',
    insight: 'Night operations (10 PM - 4 AM) have increased by 200% due to new night-time delivery regulations.',
    suggestion: 'Enhance night-time navigation infrastructure (beacons, 5G coverage).',
    chartType: 'Polar',
    chartData: Array.from({ length: 24 }, (_, i) => ({
      hour: `${i}:00`,
      value: (i > 8 && i < 18) ? randomInt(800, 1000) : randomInt(100, 300),
    })),
    keyMetrics: [
      { label: 'Peak Hour', value: '14:00' },
      { label: 'Night Share', value: '15%' },
      { label: '24h Active', value: 'Yes' },
    ]
  },
  {
    id: '09',
    title: 'Seasonal Stability Index',
    subtitle: 'Monthly Flight Volatility',
    dimension: Dimension.TimeSpace,
    value: 0.88,
    unit: 'Stability',
    trend: 0.03,
    definition: '1 - CV of monthly flight data. Measures resistance to weather/seasonal interference.',
    insight: 'Operations remained stable despite the rainy season in June, proving the robustness of the new IP54 rated fleet.',
    suggestion: 'Develop protocols for extreme wind conditions to further improve stability.',
    chartType: 'BoxPlot',
    chartData: months.map(m => ({
      name: m,
      min: randomInt(300, 400),
      avg: randomInt(450, 550),
      max: randomInt(600, 800),
    })),
    keyMetrics: [
      { label: 'Most Stable', value: 'Oct' },
      { label: 'Least Stable', value: 'Jun' },
      { label: 'Weather Impact', value: 'Low' },
    ]
  },
];

// 4. Efficiency & Quality
export const getEfficiencyQualityData = (): MetricData[] => [
  {
    id: '10',
    title: 'Per-Unit Efficiency Index',
    subtitle: 'Sorties Per Active Aircraft',
    dimension: Dimension.EfficiencyQuality,
    value: 320,
    unit: 'Sorties/Year',
    trend: 0.15,
    definition: 'Average number of flights per active drone per year.',
    insight: 'Efficiency spiked after the introduction of automated battery swapping stations.',
    suggestion: 'Deploy more automated docks to reduce turnaround time.',
    chartType: 'Gauge',
    chartData: [{ name: 'Efficiency', value: 75 }],
    keyMetrics: [
      { label: 'Avg Sorties', value: '320' },
      { label: 'Industry Avg', value: '210' },
      { label: 'Utilization', value: 'High' },
    ]
  },
  {
    id: '11',
    title: 'Long-Endurance Mission Index',
    subtitle: 'High-Value Mission Ratio',
    dimension: Dimension.EfficiencyQuality,
    value: 28,
    unit: '%',
    trend: 0.05,
    definition: 'Percentage of flights lasting longer than 30 minutes.',
    insight: 'Long-endurance flights for powerline inspection and mapping are growing steadily.',
    suggestion: 'Incentivize long-range BVLOS operations.',
    chartType: 'Funnel',
    chartData: [
      { name: '< 10 mins', value: 4000, fill: '#94a3b8' },
      { name: '10-30 mins', value: 3000, fill: '#64748b' },
      { name: '30-60 mins', value: 1500, fill: '#0ea5e9' },
      { name: '> 60 mins', value: 500, fill: '#0284c7' },
    ],
    keyMetrics: [
      { label: '>30min Share', value: '28%' },
      { label: 'Avg Duration', value: '22min' },
      { label: 'Max Duration', value: '145min' },
    ]
  },
  {
    id: '12',
    title: 'Wide-Area Coverage Index',
    subtitle: 'Flight Range Distribution',
    dimension: Dimension.EfficiencyQuality,
    value: 12.5,
    unit: 'km (Avg)',
    trend: 0.08,
    definition: 'Weighted average single flight distance.',
    insight: 'Transition from VLOS to BVLOS is evident, with 10km+ flights doubling year-over-year.',
    suggestion: 'Upgrade communication links to 5G-A to support broader coverage.',
    chartType: 'Histogram',
    chartData: [
      { name: '0-1km', value: 30 },
      { name: '1-5km', value: 45 },
      { name: '5-15km', value: 15 },
      { name: '15km+', value: 10 },
    ],
    keyMetrics: [
      { label: 'BVLOS Rate', value: '25%' },
      { label: 'Avg Range', value: '12.5km' },
      { label: 'Max Range', value: '45km' },
    ]
  },
];

// 5. Innovation & Integration
export const getInnovationData = (): MetricData[] => [
  {
    id: '13',
    title: 'Urban Micro-Circulation Index',
    subtitle: 'Cross-District Connectivity',
    dimension: Dimension.InnovationIntegration,
    value: 0.65,
    unit: 'Connectivity',
    trend: 0.2,
    definition: 'Measures the density and volume of cross-district flights, acting as "capillaries" of the city.',
    insight: 'The "South-North" logistics corridor is the busiest, accounting for 40% of cross-district traffic.',
    suggestion: 'Open new air corridors between East and West districts.',
    chartType: 'Chord',
    chartData: [
        { x: 'A', y: 'A', value: 0 }, { x: 'A', y: 'B', value: 80 }, { x: 'A', y: 'C', value: 20 },
        { x: 'B', y: 'A', value: 70 }, { x: 'B', y: 'B', value: 0 }, { x: 'B', y: 'C', value: 50 },
        { x: 'C', y: 'A', value: 30 }, { x: 'C', y: 'B', value: 60 }, { x: 'C', y: 'C', value: 0 },
    ],
    keyMetrics: [
      { label: 'Cross-Dist Vol', value: '45%' },
      { label: 'Top Route', value: 'A <-> B' },
      { label: 'Connected Pairs', value: '12' },
    ]
  },
  {
    id: '14',
    title: 'Stereoscopic Airspace Efficiency',
    subtitle: 'Vertical Airspace Utilization',
    dimension: Dimension.InnovationIntegration,
    value: 0.72,
    unit: 'Entropy',
    trend: 0.05,
    definition: 'Uniformity of flight distribution across different altitude layers (0-120m, 120-300m, 300m+).',
    insight: 'Airspace is well-stratified. Logistics prefer 100-150m, while surveys occupy 200m+.',
    suggestion: 'Keep 0-50m clear for noise reduction near residential zones.',
    chartType: '3DBar',
    chartData: [
      { name: '0-100m', value: 4000 },
      { name: '100-300m', value: 2500 },
      { name: '300m+', value: 800 },
    ],
    keyMetrics: [
      { label: 'Low Altitude', value: '55%' },
      { label: 'Mid Altitude', value: '34%' },
      { label: 'High Altitude', value: '11%' },
    ]
  },
  {
    id: '15',
    title: 'Production/Consumption Attribute',
    subtitle: 'Weekday vs. Weekend Activity',
    dimension: Dimension.InnovationIntegration,
    value: 1.4,
    unit: 'Ratio',
    trend: 0.02,
    definition: 'Ratio of Weekday Avg Sorties to Weekend Avg Sorties. >1.2 implies Production, <0.8 implies Consumption.',
    insight: 'Ratio of 1.4 confirms a "Production-Driven" economy (Logistics/Inspection).',
    suggestion: 'Promote weekend tourism flights to balance the ratio towards 1.0 (Mixed).',
    chartType: 'Calendar',
    chartData: Array.from({ length: 365 }, (_, i) => {
      const date = new Date(2023, 0, 1);
      date.setDate(date.getDate() + i);
      const iso = date.toISOString().split('T')[0];
      const day = date.getDay(); // 0 Sun, 6 Sat
      const isWeekend = day === 0 || day === 6;
      // Weekday avg ~850, Weekend ~600 to show "Production" nature
      const base = isWeekend ? 600 : 850;
      const noise = Math.floor(Math.random() * 200) - 100;
      return {
        date: iso,
        value: Math.max(0, base + noise)
      };
    }),
    keyMetrics: [
      { label: 'Type', value: 'Production' },
      { label: 'Weekday Avg', value: '850' },
      { label: 'Weekend Avg', value: '600' },
    ]
  },
  {
    id: '16',
    title: 'Low-Altitude Night Economy Index',
    subtitle: 'Night-time Flight Share',
    dimension: Dimension.InnovationIntegration,
    value: 18.5,
    unit: '%',
    trend: 0.35,
    definition: 'Percentage of flights occurring between 19:00 and 06:00.',
    insight: 'Night delivery is booming. Activity spikes at 21:00 for food delivery.',
    suggestion: 'Ensure noise compliance for night operations.',
    chartType: 'Wave',
    chartData: Array.from({ length: 24 }, (_, i) => ({
      hour: i,
      value: (i >= 19 || i <= 6) ? randomInt(300, 600) : randomInt(100, 200),
      isNight: (i >= 19 || i <= 6)
    })),
    keyMetrics: [
      { label: 'Night Share', value: '18.5%' },
      { label: 'Growth', value: '+35%' },
      { label: 'Peak Time', value: '21:00' },
    ]
  },
  {
    id: '17',
    title: 'Leading Entity Impact Index',
    subtitle: 'Top Enterprise Tech Leadership',
    dimension: Dimension.InnovationIntegration,
    value: 88,
    unit: 'Score',
    trend: 0.1,
    definition: 'Market share of Top 5 enterprises in "Difficult Tasks" (Long Range, High Altitude, Night).',
    insight: 'Top players are taking 88% of the complex missions, leaving simple tasks to smaller players.',
    suggestion: 'Support tech transfer from leaders to SMEs.',
    chartType: 'Radar',
    chartData: [
      { subject: 'Range', A: 120, B: 110, fullMark: 150 },
      { subject: 'Duration', A: 98, B: 130, fullMark: 150 },
      { subject: 'Night', A: 86, B: 130, fullMark: 150 },
      { subject: 'Load', A: 99, B: 100, fullMark: 150 },
      { subject: 'Speed', A: 85, B: 90, fullMark: 150 },
    ],
    keyMetrics: [
      { label: 'Tech Lead', value: 'High' },
      { label: 'Dominance', value: '88%' },
      { label: 'Ent. A', value: 'Rank 1' },
    ]
  },
  {
    id: '18',
    title: 'Low-Altitude Composite Prosperity',
    subtitle: 'LA-PI (Composite Index)',
    dimension: Dimension.InnovationIntegration,
    value: 82.4,
    unit: 'Points',
    trend: 0.04,
    definition: 'Weighted summary of all indicators: Scale(40%) + Structure(20%) + Innovation(20%) + TimeSpace(10%) + Efficiency(10%).',
    insight: 'The city has reached a "High Growth" phase. Infrastructure is catching up with demand.',
    suggestion: 'Focus on "Efficiency" metrics in the next quarter to boost the score above 85.',
    chartType: 'Dashboard',
    chartData: [{ name: 'Score', value: 82.4 }],
    keyMetrics: [
      { label: 'Current', value: '82.4' },
      { label: 'MoM', value: '+1.2' },
      { label: 'YoY', value: '+8.5' },
    ]
  },
];

export const getAllData = (): MetricData[] => [
  ...getScaleGrowthData(),
  ...getStructureEntityData(),
  ...getTimeSpaceData(),
  ...getEfficiencyQualityData(),
  ...getInnovationData(),
];

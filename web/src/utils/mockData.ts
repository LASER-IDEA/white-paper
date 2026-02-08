import { Dimension, MetricData } from '../types';

// Helpers
const randomInt = (min: number, max: number) => Math.floor(Math.random() * (max - min + 1) + min);

const months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'];

// 1. Scale & Growth
export const getScaleGrowthData = (): MetricData[] => [
  {
    id: '01',
    title: '低空交通流量指数',
    subtitle: '月均架次指数趋势',
    dimension: Dimension.ScaleGrowth,
    value: 112.4,
    unit: '指数',
    trend: 0.12,
    definition: '以基期月均架次为100，衡量当期月均架次的相对规模。',
    insight: '交通量呈现持续上升趋势，在年中物流节期间达到峰值。周末物流航班减少，但旅游观光航班增加。',
    suggestion: '建议扩建基础设施容量，以应对第四季度的预期高峰负荷。',
    chartType: 'Area',
    chartData: months.map((m, i) => ({
      date: `2023-${String(i + 1).padStart(2, '0')}`,
      value: 95 + i * 2 + randomInt(-3, 4),
    })),
    keyMetrics: [
      { label: '年度累计架次', value: '120万' },
      { label: '单日峰值', value: '15,400' },
      { label: '同比增长', value: '+24%' },
    ]
  },
  {
    id: '02',
    title: '运行强度指数',
    subtitle: '飞行时长与里程关联度',
    dimension: Dimension.ScaleGrowth,
    value: 108.6,
    unit: '指数',
    trend: 0.08,
    definition: '加权计算单位时间飞行时长与里程，相对基期归一化为指数。',
    insight: '里程增长快于时长，表明新型无人机机型的飞行速度和效率更高。',
    suggestion: '鼓励长距离物流航线，进一步提升该指数。',
    chartType: 'DualLine',
    chartData: months.map(m => {
      const duration = randomInt(4000, 6000) + (months.indexOf(m) * 200);
      const distance = randomInt(12000, 18000) + (months.indexOf(m) * 800);
      const speed = Math.round((distance / duration) * 10) / 10;
      return {
        name: m,
        duration,
        distance,
        speed,
      };
    }),
    keyMetrics: [
      { label: '总时长', value: '5.8万小时' },
      { label: '总里程', value: '240万公里' },
      { label: '平均速度', value: '41 km/h' },
    ]
  },
  {
    id: '03',
    title: '活跃运力规模指数',
    subtitle: '活跃航空器分类统计',
    dimension: Dimension.ScaleGrowth,
    value: 3240,
    unit: '活跃架数',
    trend: 0.25,
    definition: '当前月/季度内有飞行记录的唯一航空器序列号数量。',
    insight: '多旋翼无人机在机队中占主导地位，但垂直起降固定翼飞机采用率增长最快（环比增长40%）。',
    suggestion: '为不断增长的固定翼机队准备维护中心。',
    chartType: 'StackedBar',
    chartData: months.map(m => ({
      name: m,
      MultiRotor: randomInt(1500, 2000) + (months.indexOf(m) * 50),
      FixedWing: randomInt(200, 500) + (months.indexOf(m) * 30),
      Helicopter: randomInt(50, 100),
    })),
    keyMetrics: [
      { label: '多旋翼', value: '78%' },
      { label: '固定翼', value: '18%' },
      { label: '其他', value: '4%' },
    ]
  },
  {
    id: '04',
    title: '增长动能指数',
    subtitle: '月度增长率趋势',
    dimension: Dimension.ScaleGrowth,
    value: 6.8,
    unit: '%',
    trend: 0.03,
    definition: '月度总架次的环比/同比增速，反映规模扩张速度与趋势强度。',
    insight: '二季度增速显著提升，物流与测绘需求拉动明显。',
    suggestion: '保持运力投放节奏，避免在淡季出现运力冗余。',
    chartType: 'Area',
    chartData: months.map((m, i) => ({
      date: `2023-${String(i + 1).padStart(2, '0')}`,
      value: randomInt(-5, 18),
    })),
    keyMetrics: [
      { label: '最新环比', value: '+6.8%' },
      { label: '峰值增速', value: '+18%' },
      { label: '低谷增速', value: '-3%' },
    ]
  },
];

// 2. Structure & Entity
export const getStructureEntityData = (): MetricData[] => [
  {
    id: '05',
    title: '市场集中度指数 (CR50)',
    subtitle: '前50强企业市场份额',
    dimension: Dimension.StructureEntity,
    value: 'CR50=68%',
    unit: '',
    trend: -0.05,
    definition: '前10名或前50名企业贡献的总飞行量百分比。',
    insight: '随着新的物流初创公司进入该领域，市场正从寡头垄断转向竞争更激烈的格局。',
    suggestion: '促进中小企业创新，防止科技巨头过度垄断。',
    chartType: 'Pareto',
    chartData: Array.from({ length: 15 }, (_, i) => {
      const vol = 1000 - (i * 50) + randomInt(-20, 20);
      return {
        name: `企业${String.fromCharCode(65 + i)}`,
        volume: vol,
      };
    }),
    keyMetrics: [
      { label: 'Top 1 份额', value: '18%' },
      { label: 'Top 10 份额', value: '62%' },
      { label: '主体总数', value: '450' },
    ]
  },
  {
    id: '06',
    title: '商业成熟度指数',
    subtitle: '用户类型分布',
    dimension: Dimension.StructureEntity,
    value: 72,
    unit: '%',
    trend: 0.1,
    definition: '企业用户飞行架次占总飞行架次的比例。',
    insight: '企业用途已超过70%，标志着商业生态系统的成熟。政府用途保持稳定。',
    suggestion: '简化商业主体的空域审批流程，以保持这一势头。',
    chartType: 'Rose',
    chartData: [
      { name: '物流(企业)', value: 45 },
      { name: '巡检(企业)', value: 25 },
      { name: '个人/娱乐', value: 20 },
      { name: '政务/应急', value: 10 },
    ],
    keyMetrics: [
      { label: '商业', value: '70%' },
      { label: '消费', value: '20%' },
      { label: '公共', value: '10%' },
    ]
  },
  {
    id: '07',
    title: '机型生态多元指数',
    subtitle: '航空器型号分布',
    dimension: Dimension.StructureEntity,
    value: 0.85,
    unit: '辛普森指数',
    trend: 0.02,
    definition: '基于航空器型号飞行量计算的辛普森多样性指数。',
    insight: '高度多样性表明生态系统健康，拥有针对不同垂直领域（配送与测绘）的专用航空器。',
    suggestion: '鼓励研发专用的重载无人机。',
    chartType: 'Treemap',
    chartData: [
      { name: 'DJI M300', size: 4000, fill: '#0ea5e9' },
      { name: 'Autel Dragonfish', size: 2500, fill: '#0284c7' },
      { name: 'XAG P100', size: 2000, fill: '#10b981' },
      { name: 'Vertical V50', size: 1500, fill: '#059669' },
      { name: 'EHang 216', size: 800, fill: '#6366f1' },
      { name: '其他', size: 3000, fill: '#94a3b8' },
    ],
    keyMetrics: [
      { label: '主导机型', value: 'DJI M300' },
      { label: '机型数量', value: '42' },
      { label: '专用机型', value: '35%' },
    ]
  },
];

// 3. Time & Space
export const getTimeSpaceData = (): MetricData[] => [
  {
    id: '08',
    title: '区域平衡指数',
    subtitle: '地理飞行密度平衡',
    dimension: Dimension.TimeSpace,
    value: 0.68,
    unit: '均衡度',
    trend: 0.0,
    definition: '1 - 区域飞行架次占比的基尼系数，越高越均衡。',
    insight: '南山区和宝安区飞行密度最高，主要集中在高新科技园区和物流枢纽。盐田区密度最低。',
    suggestion: '加大盐田区等外围地区的无人机基础设施建设，提升区域平衡性。',
    chartType: 'Map',
    chartData: [
      { name: '南山区', value: 85 },
      { name: '福田区', value: 60 },
      { name: '罗湖区', value: 30 },
      { name: '宝安区', value: 95 },
      { name: '龙岗区', value: 20 },
      { name: '盐田区', value: 15 },
    ],
    keyMetrics: [
      { label: '最热区域', value: 'D区' },
      { label: '最冷区域', value: 'E区' },
      { label: '基尼系数', value: '0.32' },
    ]
  },
  {
    id: '09',
    title: '全天候运行指数',
    subtitle: '24小时飞行分布',
    dimension: Dimension.TimeSpace,
    value: 2.85,
    unit: '熵值',
    trend: 0.12,
    definition: '基于24小时分布的信息熵。数值越高意味着昼夜均有飞行。',
    insight: '受夜间配送新规影响，夜间作业（晚10点-早4点）增长了200%。',
    suggestion: '加强夜间导航基础设施（信标、5G覆盖）。',
    chartType: 'Polar',
    chartData: Array.from({ length: 24 }, (_, i) => ({
      hour: `${i}:00`,
      value: (i > 8 && i < 18) ? randomInt(800, 1000) : randomInt(100, 300),
    })),
    keyMetrics: [
      { label: '峰值时段', value: '14:00' },
      { label: '夜间占比', value: '15%' },
      { label: '全天候活跃', value: '是' },
    ]
  },
  {
    id: '10',
    title: '季节稳定性指数',
    subtitle: '月度飞行波动性',
    dimension: Dimension.TimeSpace,
    value: 0.92,
    unit: '稳定性',
    trend: 0.03,
    definition: '1 - 月度飞行数据的变异系数。衡量对天气/季节干扰的抵抗力。',
    insight: '尽管6月是雨季，运营仍保持稳定，证明了新型IP54防护等级机队的稳健性。',
    suggestion: '制定极端风况下的协议，进一步提高稳定性。',
    chartType: 'BoxPlot',
    chartData: months.map(m => ({
      name: m,
      min: randomInt(300, 400),
      avg: randomInt(450, 550),
      max: randomInt(600, 800),
    })),
    keyMetrics: [
      { label: '最稳定', value: '10月' },
      { label: '最不稳定', value: '6月' },
      { label: '天气影响', value: '低' },
    ]
  },
  {
    id: '11',
    title: '网络化枢纽指数',
    subtitle: '起降点连接度与流量',
    dimension: Dimension.TimeSpace,
    value: 82,
    unit: '枢纽度',
    trend: 0.06,
    definition: '基于起降点航线网络的连接度与流量加权得分。',
    insight: '宝安区与南山区形成双核心枢纽，承担超过45%的跨区流量。',
    suggestion: '优先在宝安与南山布局起降点与维护设施。',
    chartType: 'Graph',
    chartData: {
      categories: [
        { name: '核心枢纽' },
        { name: '次级枢纽' },
        { name: '一般枢纽' },
      ],
      nodes: [
        { name: '宝安区', value: 88, symbolSize: 46, category: 0 },
        { name: '南山区', value: 76, symbolSize: 40, category: 0 },
        { name: '福田区', value: 62, symbolSize: 34, category: 1 },
        { name: '龙岗区', value: 54, symbolSize: 30, category: 1 },
        { name: '罗湖区', value: 38, symbolSize: 24, category: 2 },
      ],
      links: [
        { source: '宝安区', target: '南山区', value: 45 },
        { source: '南山区', target: '福田区', value: 28 },
        { source: '宝安区', target: '龙岗区', value: 22 },
        { source: '福田区', target: '罗湖区', value: 16 },
        { source: '龙岗区', target: '罗湖区', value: 12 },
      ]
    },
    keyMetrics: [
      { label: '核心枢纽', value: '宝安区' },
      { label: '次级枢纽', value: '南山区' },
      { label: '枢纽数', value: '5' },
    ]
  },
];

// 4. Efficiency & Quality
export const getEfficiencyQualityData = (): MetricData[] => [
  {
    id: '12',
    title: '单机效率指数',
    subtitle: '活跃航空器人均架次',
    dimension: Dimension.EfficiencyQuality,
    value: 320,
    unit: '架次/年',
    trend: 0.15,
    definition: '每架活跃无人机每年的平均飞行次数。',
    insight: '引入自动换电站后，效率飙升。',
    suggestion: '部署更多自动机库以减少周转时间。',
    chartType: 'Gauge',
    chartData: [{ name: '效率', value: 75 }],
    keyMetrics: [
      { label: '平均架次', value: '320' },
      { label: '行业平均', value: '210' },
      { label: '利用率', value: '高' },
    ]
  },
  {
    id: '13',
    title: '长航时任务指数',
    subtitle: '高价值任务比例',
    dimension: Dimension.EfficiencyQuality,
    value: 28,
    unit: '%',
    trend: 0.05,
    definition: '飞行时长超过30分钟的航班比例。',
    insight: '用于电力巡检和测绘的长航时飞行稳步增长。',
    suggestion: '激励长距离超视距（BVLOS）作业。',
    chartType: 'Funnel',
    chartData: [
      { name: '< 10 分钟', value: 4000, fill: '#94a3b8' },
      { name: '10-30 分钟', value: 3000, fill: '#64748b' },
      { name: '30-60 分钟', value: 1500, fill: '#0ea5e9' },
      { name: '> 60 分钟', value: 500, fill: '#0284c7' },
    ],
    keyMetrics: [
      { label: '>30分钟占比', value: '28%' },
      { label: '平均时长', value: '22分钟' },
      { label: '最大时长', value: '145分钟' },
    ]
  },
  {
    id: '14',
    title: '广域覆盖指数',
    subtitle: '飞行航程分布',
    dimension: Dimension.EfficiencyQuality,
    value: 12.5,
    unit: '公里 (平均)',
    trend: 0.08,
    definition: '加权平均单次飞行距离。',
    insight: '从视距内（VLOS）向超视距（BVLOS）的转变明显，10公里以上的飞行同比翻倍。',
    suggestion: '升级通信链路至5G-A以支持更广泛的覆盖。',
    chartType: 'Histogram',
    chartData: [
      { name: '0-1km', value: 30 },
      { name: '1-5km', value: 45 },
      { name: '5-15km', value: 15 },
      { name: '15km+', value: 10 },
    ],
    keyMetrics: [
      { label: '超视距率', value: '25%' },
      { label: '平均航程', value: '12.5km' },
      { label: '最大航程', value: '45km' },
    ]
  },
  {
    id: '15',
    title: '任务完成质量指数',
    subtitle: '有效飞行完成率',
    dimension: Dimension.EfficiencyQuality,
    value: 92.3,
    unit: '%',
    trend: 0.04,
    definition: '实际完成的有效飞行架次与计划报备架次的比率。',
    insight: '质量指数处于高位，说明飞行计划执行稳定。',
    suggestion: '持续优化航线调度与异常预警，降低计划偏差。',
    chartType: 'ControlChart',
    chartData: {
      latestTqi: 92.3,
      // 航迹偏离度控制图数据（24小时）
      trajData: [
        { time: '00:00', deviation: 0.08, mean: 0.0, ucl: 0.25, lcl: -0.25 },
        { time: '02:00', deviation: -0.05, mean: 0.0, ucl: 0.25, lcl: -0.25 },
        { time: '04:00', deviation: 0.12, mean: 0.0, ucl: 0.25, lcl: -0.25 },
        { time: '06:00', deviation: 0.15, mean: 0.0, ucl: 0.25, lcl: -0.25 },
        { time: '08:00', deviation: 0.22, mean: 0.0, ucl: 0.25, lcl: -0.25 },
        { time: '10:00', deviation: 0.18, mean: 0.0, ucl: 0.25, lcl: -0.25 },
        { time: '12:00', deviation: 0.28, mean: 0.0, ucl: 0.25, lcl: -0.25 }, // 超限点
        { time: '14:00', deviation: 0.20, mean: 0.0, ucl: 0.25, lcl: -0.25 },
        { time: '16:00', deviation: 0.10, mean: 0.0, ucl: 0.25, lcl: -0.25 },
        { time: '18:00', deviation: 0.05, mean: 0.0, ucl: 0.25, lcl: -0.25 },
        { time: '20:00', deviation: -0.03, mean: 0.0, ucl: 0.25, lcl: -0.25 },
        { time: '22:00', deviation: 0.02, mean: 0.0, ucl: 0.25, lcl: -0.25 },
      ],
      // TQI 历史趋势（30天）
      tqiHistory: [
        { time: '01-01', tqi: 88.5, mean: 90, ucl: 98, lcl: 75 },
        { time: '01-05', tqi: 89.2, mean: 90, ucl: 98, lcl: 75 },
        { time: '01-08', tqi: 91.0, mean: 90, ucl: 98, lcl: 75 },
        { time: '01-12', tqi: 90.5, mean: 90, ucl: 98, lcl: 75 },
        { time: '01-15', tqi: 92.3, mean: 90, ucl: 98, lcl: 75 },
        { time: '01-18', tqi: 93.1, mean: 90, ucl: 98, lcl: 75 },
        { time: '01-22', tqi: 91.8, mean: 90, ucl: 98, lcl: 75 },
        { time: '01-25', tqi: 92.5, mean: 90, ucl: 98, lcl: 75 },
        { time: '01-27', tqi: 92.3, mean: 90, ucl: 98, lcl: 75 },
      ],
      // 计划 vs 实际（30天）
      planActual: [
        { time: '01-01', actual: 445, planned: 500 },
        { time: '01-05', actual: 468, planned: 520 },
        { time: '01-08', actual: 520, planned: 560 },
        { time: '01-12', actual: 485, planned: 530 },
        { time: '01-15', actual: 540, planned: 580 },
        { time: '01-18', actual: 565, planned: 600 },
        { time: '01-22', actual: 498, planned: 540 },
        { time: '01-25', actual: 525, planned: 560 },
        { time: '01-27', actual: 510, planned: 550 },
      ]
    },
    keyMetrics: [
      { label: '完成率', value: '92.3%' },
      { label: '偏差率', value: '7.7%' },
      { label: '稳定性', value: '高' },
    ]
  },
];

// 5. Innovation & Integration
export const getInnovationData = (): MetricData[] => [
  {
    id: '16',
    title: '城市微循环指数',
    subtitle: '跨区连通性',
    dimension: Dimension.InnovationIntegration,
    value: 0.65,
    unit: '连通度',
    trend: 0.2,
    definition: '衡量跨区飞行的密度和数量，充当城市的“毛细血管”。',
    insight: '“南-北”物流走廊最繁忙，占跨区流量的40%。',
    suggestion: '开通东西区之间的新空中走廊。',
    chartType: 'Chord',
    chartData: [
        { x: 'A区', y: 'A区', value: 0 }, { x: 'A区', y: 'B区', value: 80 }, { x: 'A区', y: 'C区', value: 20 },
        { x: 'B区', y: 'A区', value: 70 }, { x: 'B区', y: 'B区', value: 0 }, { x: 'B区', y: 'C区', value: 50 },
        { x: 'C区', y: 'A区', value: 30 }, { x: 'C区', y: 'B区', value: 60 }, { x: 'C区', y: 'C区', value: 0 },
    ],
    keyMetrics: [
      { label: '跨区流量', value: '45%' },
      { label: '热门航线', value: 'A区 <-> B区' },
      { label: '连通对', value: '12' },
    ]
  },
  {
    id: '17',
    title: '立体空域效率',
    subtitle: '垂直空域利用率',
    dimension: Dimension.InnovationIntegration,
    value: 0.72,
    unit: '熵值',
    trend: 0.05,
    definition: '不同高度层飞行分布的均匀度，按区域和高度层细分。',
    insight: '空域分层良好。物流偏好100-150m，而测绘占据200m+。宝安区和南山区在各个高度层的活动最为活跃。',
    suggestion: '保持0-50m净空，以减少居民区附近的噪音。加强中高空域的协调管理。',
    chartType: 'GroupedBar',
    chartData: {
      // Grouped bar chart data structure: [x_axis_index, y_axis_index, value]
      // x: altitude layers, y: districts
      districts: ['宝安区', '南山区', '福田区', '龙岗区', '罗湖区', '盐田区'],
      altitudes: ['0-50m', '50-100m', '100-150m', '150-200m', '200-250m', '250-300m', '300m+'],
      data: [
        // 宝安区 (District 0)
        [0, 0, 320], [1, 0, 850], [2, 0, 1200], [3, 0, 680], [4, 0, 420], [5, 0, 280], [6, 0, 150],
        // 南山区 (District 1)
        [0, 1, 280], [1, 1, 720], [2, 1, 980], [3, 1, 590], [4, 1, 380], [5, 1, 250], [6, 1, 120],
        // 福田区 (District 2)
        [0, 2, 180], [1, 2, 520], [2, 2, 680], [3, 2, 420], [4, 2, 280], [5, 2, 180], [6, 2, 80],
        // 龙岗区 (District 3)
        [0, 3, 120], [1, 3, 380], [2, 3, 520], [3, 3, 320], [4, 3, 210], [5, 3, 140], [6, 3, 60],
        // 罗湖区 (District 4)
        [0, 4, 90], [1, 4, 280], [2, 4, 380], [3, 4, 240], [4, 4, 160], [5, 4, 110], [6, 4, 50],
        // 盐田区 (District 5)
        [0, 5, 50], [1, 5, 150], [2, 5, 200], [3, 5, 130], [4, 5, 90], [5, 5, 60], [6, 5, 30],
      ]
    },
    keyMetrics: [
      { label: '100-150m层', value: '41%' },
      { label: '50-100m层', value: '32%' },
      { label: '其他高度', value: '27%' },
    ]
  },
  {
    id: '18',
    title: '低空经济“生产/消费”属性指数',
    subtitle: '工作日与周末活动对比',
    dimension: Dimension.InnovationIntegration,
    value: 1.4,
    unit: '比率',
    trend: 0.02,
    definition: '工作日日均架次与周末日均架次的比率。>1.2 意味着生产型，<0.8 意味着消费型。',
    insight: '1.4的比率证实了“生产驱动”型经济（物流/巡检）。',
    suggestion: '推广周末旅游观光飞行，使比率向1.0（混合型）平衡。',
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
      { label: '类型', value: '生产型' },
      { label: '工作日均值', value: '850' },
      { label: '周末均值', value: '600' },
    ]
  },
  {
    id: '19',
    title: '低空夜间经济指数',
    subtitle: '夜间飞行占比',
    dimension: Dimension.InnovationIntegration,
    value: 18.5,
    unit: '%',
    trend: 0.35,
    definition: '发生在19:00至06:00之间的飞行百分比。',
    insight: '夜间配送蓬勃发展。食品配送活动在21:00达到高峰。',
    suggestion: '确保夜间运行符合噪音标准。',
    chartType: 'Wave',
    chartData: Array.from({ length: 24 }, (_, i) => ({
      hour: i,
      value: (i >= 19 || i <= 6) ? randomInt(300, 600) : randomInt(100, 200),
      isNight: (i >= 19 || i <= 6)
    })),
    keyMetrics: [
      { label: '夜间占比', value: '18.5%' },
      { label: '增长', value: '+35%' },
      { label: '峰值时间', value: '21:00' },
    ]
  },
  {
    id: '20',
    title: '龙头主体影响力指数',
    subtitle: '头部企业技术领导力',
    dimension: Dimension.InnovationIntegration,
    value: 88,
    unit: '得分',
    trend: 0.1,
    definition: '前5名企业在“高难任务”（长航程、高海拔、夜间）中的市场份额。',
    insight: '头部玩家承担了88%的复杂任务，将简单任务留给较小的玩家。',
    suggestion: '支持从龙头企业向中小企业的技术转移。',
    chartType: 'Radar',
    chartData: [
      { subject: '航程', A: 120, B: 110, fullMark: 150 },
      { subject: '时长', A: 98, B: 130, fullMark: 150 },
      { subject: '夜间', A: 86, B: 130, fullMark: 150 },
      { subject: '载重', A: 99, B: 100, fullMark: 150 },
      { subject: '速度', A: 85, B: 90, fullMark: 150 },
    ],
    keyMetrics: [
      { label: '技术领先', value: '高' },
      { label: '主导地位', value: '88%' },
      { label: '企业 A', value: '排名第1' },
    ]
  },
  {
    id: '21',
    title: '低空综合繁荣度',
    subtitle: 'LA-PI (综合指数)',
    dimension: Dimension.InnovationIntegration,
    value: 82.4,
    unit: '分',
    trend: 0.04,
    definition: '所有指标的加权汇总：规模(40%) + 结构(20%) + 创新(20%) + 时空(10%) + 效率(10%)。',
    insight: '城市已进入“高增长”阶段。基础设施正赶上需求。',
    suggestion: '下个季度重点关注“效率”指标，将得分提升至85以上。',
    chartType: 'Dashboard',
    chartData: [{ name: '得分', value: 82.4 }],
    keyMetrics: [
      { label: '当前得分', value: '82.4' },
      { label: '环比', value: '+1.2' },
      { label: '同比', value: '+8.5' },
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

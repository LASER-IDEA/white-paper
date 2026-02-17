# 用户研究数据分析计划

## 分析目标

1. 量化对比 LAEV-Agents 和 NL4DV 的可用性差异
2. 识别系统的优势和待改进之处
3. 验证研究假设
4. 为论文提供统计支持

## 研究假设

### 主要假设 (H1)
**H1**: LAEV-Agents 的 SUS 评分显著高于 NL4DV
- 预期: LAEV SUS > NL4DV SUS，差异具有统计显著性 (p < 0.05)

### 次要假设 (H2-H4)
**H2**: LAEV-Agents 的任务完成率高于 NL4DV
- 预期: LAEV 完成率 > NL4DV 完成率

**H3**: LAEV-Agents 的任务完成时间与 NL4DV 相当或更短
- 预期: LAEV 时间 ≤ NL4DV 时间

**H4**: 用户对 LAEV-Agents 的主观满意度更高
- 预期: LAEV 有用性评分 > NL4DV 有用性评分

## 数据预处理

### 数据清洗
1. 检查缺失值
2. 识别异常值 (完成时间 > 3个标准差)
3. SUS反向题目重新编码
4. 计算SUS总分

### 数据格式
```json
{
  "participant_id": "P001",
  "demographics": {
    "age": 25,
    "gender": "M",
    "education": "Master",
    "experience": "Intermediate"
  },
  "results": {
    "nl4dv": {
      "task1": {"success": true, "time": 120, "errors": 0},
      "task2": {"success": true, "time": 180, "errors": 1},
      "sus": [4, 2, 4, 2, 3, 2, 4, 2, 4, 2],
      "sus_score": 75
    },
    "laev": {
      "task1": {"success": true, "time": 90, "errors": 0},
      "task2": {"success": true, "time": 150, "errors": 0},
      "sus": [5, 1, 5, 1, 4, 1, 5, 1, 5, 1],
      "sus_score": 95
    }
  },
  "preference": "LAEV",
  "interview_notes": "..."
}
```

## 定量分析

### 1. 描述性统计

#### SUS评分
- 计算每个系统的均值、标准差、中位数
- 绘制箱线图对比

```python
# Python伪代码
import pandas as pd
import scipy.stats as stats

# SUS描述性统计
nl4dv_sus = df['nl4dv_sus']
laev_sus = df['laev_sus']

print(f"NL4DV: M={nl4dv_sus.mean():.1f}, SD={nl4dv_sus.std():.1f}")
print(f"LAEV:  M={laev_sus.mean():.1f}, SD={laev_sus.std():.1f}")
```

#### 任务完成率
- 计算每个系统的成功率
- 使用卡方检验比较

#### 任务完成时间
- 计算均值、标准差
- 剔除失败任务的时间
- 绘制时间分布图

### 2. 假设检验

#### H1: SUS评分差异 (配对t检验)
```python
# 配对t检验
t_stat, p_value = stats.ttest_rel(laev_sus, nl4dv_sus)
print(f"t({len(df)-1}) = {t_stat:.2f}, p = {p_value:.4f}")

# 效应量 (Cohen's d)
d = (laev_sus.mean() - nl4dv_sus.mean()) / np.sqrt(((laev_sus.var() + nl4dv_sus.var()) / 2))
print(f"Cohen's d = {d:.2f}")
```

**结果解释**:
- p < 0.05: 拒绝原假设，差异显著
- d = 0.2: 小效应
- d = 0.5: 中等效应
- d = 0.8: 大效应

#### H3: 完成时间差异 (Wilcoxon符号秩检验)
```python
# 非参数检验 (时间数据通常非正态)
statistic, p_value = stats.wilcoxon(laev_time, nl4dv_time)
print(f"W = {statistic}, p = {p_value:.4f}")
```

### 3. 子组分析

#### 按用户类型分组
- 领域专家 vs 普通用户
- 可视化经验: 高 vs 低
- 编程经验: 有 vs 无

```python
# 分组比较
experts = df[df['is_expert'] == True]
novices = df[df['is_expert'] == False]

print("Experts:")
print(f"  LAEV SUS: {experts['laev_sus'].mean():.1f}")
print(f"  NL4DV SUS: {experts['nl4dv_sus'].mean():.1f}")

print("Novices:")
print(f"  LAEV SUS: {novices['laev_sus'].mean():.1f}")
print(f"  NL4DV SUS: {novices['nl4dv_sus'].mean():.1f}")
```

### 4. 相关性分析

- SUS评分与任务完成时间的相关性
- 领域知识与系统偏好的相关性

## 定性分析

### 1. 访谈数据编码

#### 开放编码 (Open Coding)
逐行阅读访谈记录，提取关键概念:
```
引文: "LAEV能理解我的复杂查询，NL4DV经常报错"
编码: 自然语言理解能力、错误处理
```

#### 轴心编码 (Axial Coding)
将开放编码归类为主题:
- **主题1**: 自然语言理解
  - 子主题: 复杂查询处理、意图识别准确性
- **主题2**: 可视化质量
  - 子主题: 图表类型选择、美观性、可读性
- **主题3**: 系统响应
  - 子主题: 响应速度、错误反馈、迭代能力

#### 选择性编码 (Selective Coding)
识别核心主题:
- 核心主题: 领域适应性

### 2. 主题分析结果呈现

#### 正面反馈主题 (频率)
| 主题 | 提及次数 | 代表性引文 |
|------|----------|-----------|
| 自然语言理解强 | 12 | "LAEV能懂我的意思" |
| 图表质量高 | 10 | "生成的图很专业" |
| 领域知识丰富 | 8 | "能识别低空经济术语" |

#### 负面反馈主题 (频率)
| 主题 | 提及次数 | 代表性引文 |
|------|----------|-----------|
| 响应速度慢 | 5 | "等待时间有点长" |
| 交互功能少 | 4 | "希望能手动调整图表" |

### 3. 定性-定量整合

- 定性发现支持定量结果
- 定性解释定量差异的原因
- 识别定量数据未捕捉的洞察

## 可视化计划

### 1. SUS评分对比
- 并排箱线图
- 均值误差条图
- 个体变化图 (Paired plot)

### 2. 任务性能对比
- 堆叠柱状图 (成功/失败)
- 时间分布小提琴图

### 3. 系统偏好
- 饼图/环形图
- 分组柱状图 (按用户类型)

### 4. 定性主题
- 词云
- 主题网络图

## 论文报告内容

### Results 章节结构

#### 6.1 参与者特征
- 样本量: N=16-20
- 人口统计描述
- 背景信息分布

#### 6.2 可用性评估 (SUS)
- 描述性统计
- 配对t检验结果
- 效应量报告

#### 6.3 任务性能
- 完成率对比
- 完成时间对比
- 错误分析

#### 6.4 用户偏好
- 系统选择比例
- 实际使用意愿

#### 6.5 定性发现
- 主题分析结果
- 代表性引文
- 改进建议汇总

## 统计分析脚本

见 `analysis_script.py`

## 质量控制

### 数据完整性检查
- [ ] 所有参与者都有完整的SUS评分
- [ ] 所有任务都有完成状态记录
- [ ] 访谈记录完整

### 编码一致性
- [ ] 双人编码，计算Kappa系数
- [ ] 不一致处讨论达成共识

### 结果验证
- [ ] 与预期方向一致
- [ ] 统计显著性合理
- [ ] 效应量解释恰当

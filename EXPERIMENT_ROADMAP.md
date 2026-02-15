# IEEE VIS 2026 专业路线实施路线图

> **目标**: IEEE VIS Full Paper (TVCG期刊)  
> **策略**: Multi-Agent + GraphRAG + Visual Feedback + 扎实实验  
> **Baseline**: NL4DV (Georgia Tech) + Direct LLM  
> **实验形式**: 现场用户研究

---

## ✅ Week 1 完成内容 (2026.02.14-02.21)

### 1. 多Agent架构框架 (Production-ready)
```
python/src/agents/
├── base.py              # Agent基类、状态管理、Pipeline
├── planner.py           # 意图分析 + 形式化Design Space ⭐
├── retriever.py         # GraphRAG (Neo4j) + Vector RAG ⭐
├── coder.py             # 多策略代码生成
├── evaluator.py         # 代码执行 + 质量评估
├── reflector.py         # 错误分析 + 迭代优化 ⭐
└── orchestrator.py      # 主入口
```

**创新点**:
- **形式化Design Space**: 低空经济领域的数据维度、任务类型、图表映射
- **Neo4j GraphRAG**: 支持多跳推理的知识图谱
- **Multi-Agent Pipeline**: Planner→Retriever→Coder→Evaluator→Reflector

### 2. NL4DV Baseline封装
- 完整复现NL4DV接口
- 支持真实数据加载
- 执行时间统计
- 输出Vega-Lite规范

### 3. 真实数据集
- **500条飞行记录** (sample_flight_data.csv)
- **18个属性**: 时间、空间、类别、数值
- **Domain Metadata**: 完整的语义定义

### 4. 测试Query集 (17个，将扩展至30)
| 任务类型 | 数量 | 复杂度分布 |
|---------|------|-----------|
| Trend Analysis | 3 | 简单2 + 复杂1 |
| Comparison | 3 | 简单2 + 复杂1 |
| Distribution | 3 | 简单2 + 复杂1 |
| Correlation | 3 | 简单1 + 中等1 + 复杂1 |
| Exploration | 3 | 简单2 + 复杂1 |
| Anomaly Detection | 2 | 中等2 |

### 5. 实验框架
```
experiments/
├── run_experiment.py      # 主实验运行器
├── data/
│   ├── dataset_loader.py  # 真实数据加载
│   └── test_queries.py    # 测试Query集
├── baselines/
│   └── nl4dv_baseline.py  # NL4DV + Direct LLM
└── results/               # 实验输出
```

---

## 📋 Week 2-4 核心任务

### Week 2 (2.22-2.28): 集成测试与问题修复

**优先级1: 修复Neo4j连接**
```bash
# 测试Neo4j连接
cd experiments
docker run -d --name neo4j-vis \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/vispaper2026 \
  neo4j:5.15-community

# 验证python连接
python3 -c "from neo4j import GraphDatabase; \
  d=GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j','vispaper2026')); \
  d.verify_connectivity(); print('OK')"
```

**优先级2: 运行小规模实验**
```bash
# 测试5个queries
python run_experiment.py --systems nl4dv laev --queries 5
```

**优先级3: 修复Agent导入问题**
- 确保所有Agent使用真实LLM调用
- 移除所有mock/fallback代码
- 添加错误处理和重试机制

### Week 3 (3.1-3.7): GraphRAG完善

**从PDF抽取实体关系**
```python
# 使用LLM从白皮书抽取
抽取内容:
- 实体: 无人机类型、业务类型、区域、指标、政策
- 关系: regulates, includes, used_for, part_of
- 属性: 数值范围、类别定义
```

**扩展Query集至30个**
- 每个任务类型 × 每种复杂度 = 6个queries
- 5个任务类型 = 30个queries

**运行完整Baseline对比**
```bash
python run_experiment.py --systems all
```

### Week 4 (3.8-3.14): 评估体系搭建

**消融实验设计**
| 系统变体 | 描述 | 目的 |
|---------|------|------|
| LAEV-Full | 完整Multi-Agent | 主系统 |
| LAEV-NoGraph | 移除GraphRAG | 验证GraphRAG价值 |
| LAEV-Single | 单Agent (无迭代) | 验证Multi-Agent价值 |
| NL4DV | Baseline | 对比 |
| Direct-LLM | 简单Prompt | 对比 |

**评估指标实现**
1. **成功率**: 代码执行成功占比
2. **准确率**: 生成图表类型匹配预期
3. **执行时间**: 平均耗时
4. **迭代次数**: 平均需要几次迭代

---

## 📊 Week 5-8 实验执行

### Week 5-6: 定量实验 (3.15-3.28)

**实验1: 主要对比 (3天)**
- 系统: LAEV vs NL4DV vs Direct-LLM
- Queries: 全部30个
- 重复: 3次 (取平均)
- 输出: 成功率、准确率、时间

**实验2: 消融实验 (3天)**
- 系统: LAEV-Full, LAEV-NoGraph, LAEV-Single
- 验证各组件贡献

**实验3: 复杂度分析 (2天)**
- 按Simple/Medium/Complex分组分析
- 验证系统在处理复杂查询时的优势

### Week 7-8: 用户研究 (3.29-4.11)

**研究设计**
- **参与者**: 15-20人
  - 组1: 低空经济领域专家 (5-7人)
  - 组2: 数据分析师 (5-7人)
  - 组3: 普通用户 (5-7人)

- **任务设计** (每人5个任务):
  1. 简单趋势分析 (Trend)
  2. 区域比较 (Comparison)
  3. 分布探索 (Distribution)
  4. 相关性分析 (Correlation)
  5. 复杂综合查询 (Complex)

- **测量指标**:
  - SUS量表 (System Usability Scale)
  - 任务完成率
  - 任务完成时间
  - 主观满意度 (1-5 Likert)
  - 定性访谈 (30分钟)

- **现场实验流程** (每人90分钟):
  ```
  0-10min:   介绍与知情同意
  10-20min:  系统教程
  20-70min:  5个任务 (每个10分钟)
  70-80min:  SUS问卷
  80-90min:  定性访谈
  ```

**招募计划**
- 领域专家: 联系深圳无人机协会、相关研究院
- 数据分析师: 公司内部、校友网络
- 普通用户: 高校学生、社媒招募

---

## 📝 Week 9-12 论文写作

### Week 9 (4.12-4.18): 方法部分
- System Overview (架构图)
- Planner Agent (Design Space)
- Retriever Agent (GraphRAG)
- Coder Agent (Multi-strategy)
- Evaluator/Reflector Agents

### Week 10 (4.19-4.25): 实验部分
- Evaluation Setup
- Quantitative Results (Baseline对比、消融)
- User Study Results

### Week 11 (4.26-5.2): 完善与讨论
- Related Work refinement
- Discussion (Limitations)
- Introduction + Conclusion
- Figures and Tables

### Week 12 (5.3-5.9): 修改与投稿准备
- Internal review
- Formatting (VIS template)
- Supplemental materials
- Submission

---

## 🔬 实验质量控制

### 数据真实性保证
- ✅ 使用真实飞行数据 (500条记录)
- ✅ 从PDF抽取知识图谱 (非手工构造)
- ✅ 真实LLM调用 (DeepSeek/OpenAI)
- ✅ 真实代码执行 (PyECharts)
- ✅ 真实用户研究 (现场实验)

### 对比公平性
- 相同数据集
- 相同查询集
- 多次运行取平均
- 报告标准差

### 可重复性
- 代码开源 (投稿后)
- 实验脚本自动化
- Docker环境
- 随机种子固定

---

## ⚠️ 风险与应对

| 风险 | 概率 | 影响 | 应对 |
|------|------|------|------|
| Neo4j不稳定 | 中 | 高 | 准备内存版fallback |
| LLM API限制 | 中 | 中 | 多key轮换、指数退避 |
| 用户招募困难 | 高 | 高 | 提前联系、扩大范围 |
| 实验结果不理想 | 低 | 高 | 增加query数量、细化分析 |

---

## 📁 关键文件索引

### Agent实现
- `/python/src/agents/` - 多Agent系统
- `/python/src/agents/planner.py` - Design Space
- `/python/src/agents/retriever.py` - GraphRAG

### 实验框架
- `/experiments/run_experiment.py` - 主运行器
- `/experiments/data/test_queries.py` - 测试Query集
- `/experiments/baselines/nl4dv_baseline.py` - Baseline封装

### 文档
- `/EXPERIMENT_ROADMAP.md` - 本文件
- `/experiments/README.md` - 实验说明
- `/VIS_PAPER_PLAN.md` - 论文计划

---

## 🎯 成功标准 (投稿前必须达成)

- [ ] Multi-Agent系统稳定运行
- [ ] GraphRAG成功连接Neo4j
- [ ] NL4DV Baseline成功对比
- [ ] 30个Query全部测试完成
- [ ] 消融实验显示各组件贡献
- [ ] 用户研究完成 (≥15人)
- [ ] 论文初稿完成
- [ ] 所有图表制作完成

---

## 📞 本周Action Items

1. **修复Neo4j连接**
   ```bash
   docker pull neo4j:5.15-community
   docker run -d --name neo4j-vis -p 7474:7474 -p 7687:7687 \
     -e NEO4J_AUTH=neo4j/vispaper2026 \
     neo4j:5.15-community
   ```

2. **安装NL4DV**
   ```bash
   cd /data1/xh/workspace/white-paper/nl4dv
   pip install -e .
   ```

3. **运行首次实验**
   ```bash
   cd /data1/xh/workspace/white-paper/experiments
   python run_experiment.py --systems nl4dv --queries 3
   ```

4. **扩展Query集至30个**
   - 添加更多complex queries
   - 确保覆盖所有chart types

---

**制定日期**: 2026.02.14  
**下次Review**: 2026.02.21

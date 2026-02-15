# User Study Protocol
## LAEV-Agents: Multi-Agent RAG for Domain-Specific Visualization
### IEEE VIS 2026 Submission

---

## 1. Study Overview

### Purpose
Evaluate the usability, usefulness, and user satisfaction of LAEV-Agents compared to baseline systems for low-altitude economy data visualization.

### Research Questions
1. **RQ1**: Does LAEV-Agents improve task completion success rate compared to baselines?
2. **RQ2**: Do users find LAEV-Agents more usable (SUS score)?
3. **RQ3**: Do users perceive LAEV-Agents as more useful for domain-specific analysis?
4. **RQ4**: How does multi-agent interaction affect user trust and satisfaction?

### Study Design
- **Type**: Within-subjects design (each participant uses multiple systems)
- **Systems**: 3 conditions
  - Condition A: Direct LLM (baseline)
  - Condition B: LAEV-SinglePass (no iteration)
  - Condition C: LAEV-Full (multi-agent with iteration)
- **Counterbalancing**: Latin square design for system order
- **Duration**: 90 minutes per participant
- **Compensation**: ¥200 (or equivalent)

---

## 2. Participants

### Target Sample
- **N = 18** (6 per user group)
- **Power analysis**: With α=0.05, power=0.80, effect size d=0.8

### User Groups
1. **Domain Experts** (n=6)
   - Low-altitude economy researchers
   - UAV industry analysts
   - Government regulators
   - Criteria: >2 years experience in low-altitude economy domain

2. **Data Analysts** (n=6)
   - Professional data analysts
   - BI tool users
   - Data scientists
   - Criteria: Regular use of data visualization tools

3. **General Users** (n=6)
   - Graduate students
   - Business professionals
   - Non-technical users
   - Criteria: Basic familiarity with data concepts

### Recruitment Channels
- **Domain Experts**: Shenzhen UAV Association, CAAC research institutes
- **Data Analysts**: LinkedIn, company referrals, alumni networks
- **General Users**: University mailing lists, social media

### Inclusion Criteria
- Age 18-60
- Normal or corrected vision
- Can read Chinese or English
- No prior exposure to LAEV-Agents system

---

## 3. Materials

### Systems
1. **Direct LLM**: Simple chat interface with DeepSeek
2. **LAEV-SinglePass**: Multi-agent without iteration (1-pass)
3. **LAEV-Full**: Complete multi-agent with up to 3 iterations

### Dataset
- **Source**: Shenzhen low-altitude flight operations (500 records)
- **Attributes**: Time, location, aircraft type, duration, distance, purpose
- **Familiarization**: 5-minute tutorial on dataset schema

### Tasks (5 per system = 15 total)
| Task | Type | Complexity | Description |
|------|------|------------|-------------|
| T1 | Trend Analysis | Simple | Show flight trend over time |
| T2 | Comparison | Simple | Compare flight duration across regions |
| T3 | Distribution | Medium | Show flight purpose distribution by region |
| T4 | Correlation | Medium | Analyze relationship between altitude and distance |
| T5 | Complex Query | Complex | Multi-dimensional dashboard for operational efficiency |

### Questionnaires
1. **Demographics**: Age, gender, education, experience
2. **System Usability Scale (SUS)**: 10 items, 5-point Likert
3. **NASA-TLX**: Task load assessment (optional)
4. **Custom Questions**:
   - Usefulness: "This system helped me complete the task effectively" (1-5)
   - Trust: "I trust the system's output" (1-5)
   - Preference: Rank the three systems

---

## 4. Procedure

### Session Structure (90 minutes)

#### Phase 1: Introduction (10 min)
- Welcome and consent form
- Study overview
- Pre-study questionnaire (demographics)

#### Phase 2: System Tutorial (15 min)
- Dataset introduction (5 min)
- Practice task with each system (10 min)
- Questions allowed

#### Phase 3: Main Tasks (45 min)
- 5 tasks per system × 3 systems = 15 tasks
- Time limit: 3 minutes per task
- Record: Success/failure, time, number of attempts
- Randomized task order within each system

#### Phase 4: Questionnaires (15 min)
- SUS for each system
- NASA-TLX (optional)
- Custom questions
- System ranking

#### Phase 5: Interview (5 min)
- Open-ended feedback
- "What did you like most/least about each system?"
- "When would you use each system?"

### Task Instructions
```
"Your task is: [task description]

You can interact with the system using natural language.
The system will generate a visualization based on your query.

Time limit: 3 minutes
Success criteria: Generated chart correctly answers the question"
```

### Success Criteria
| Task | Success Criteria |
|------|-----------------|
| T1 | Line chart showing temporal trend |
| T2 | Bar chart comparing regions |
| T3 | Grouped visualization showing distribution |
| T4 | Scatter plot or correlation chart |
| T5 | Multi-panel dashboard or comprehensive chart |

---

## 5. Measures

### Objective Measures
| Measure | Description |
|---------|-------------|
| **Task Success** | Binary (success/failure) |
| **Task Completion Time** | Seconds from start to success |
| **Number of Attempts** | Queries submitted per task |
| **Iteration Count** | (for LAEV-Full) Number of refinement cycles |

### Subjective Measures
| Measure | Scale | Items |
|---------|-------|-------|
| **SUS** | 0-100 | 10 standard items |
| **Usefulness** | 1-5 | 3 custom items |
| **Trust** | 1-5 | 3 custom items |
| **Preference** | Rank | 1st, 2nd, 3rd choice |

### Qualitative Data
- Interview notes
- Observation notes (strategies, frustrations)
- Screen recordings (with consent)

---

## 6. Analysis Plan

### Quantitative Analysis
1. **Success Rate**: Chi-square test between systems
2. **Completion Time**: Repeated measures ANOVA
3. **SUS Scores**: Repeated measures ANOVA + pairwise t-tests
4. **Correlation**: Pearson r between SUS and task success

### Qualitative Analysis
1. Thematic analysis of interview transcripts
2. Coding: Usability issues, feature requests, trust factors
3. Affinity diagramming

### Expected Results
- **H1**: LAEV-Full > LAEV-SinglePass > Direct LLM in success rate
- **H2**: LAEV-Full has higher SUS score than baselines
- **H3**: Domain experts show stronger preference for LAEV-Full
- **H4**: Iteration feature increases user trust

---

## 7. Ethical Considerations

### Ethics Approval
- Apply for IRB approval from host institution
- Informed consent required
- Right to withdraw at any time

### Data Protection
- Anonymize all participant data
- Store data securely (encrypted)
- Retention: 3 years post-publication
- No personally identifiable information in publications

### Risk Assessment
- **Minimal risk**: Standard software usability study
- **Mitigation**: Breaks provided, supportive environment

---

## 8. Logistics

### Equipment
- Laptop with 3 system variants installed
- 24-inch external monitor (optional)
- Audio recorder for interviews
- Stopwatch for timing

### Venue
- Quiet lab room
- Separate observation area (for note-taking)
- Whiteboard for debriefing

### Schedule
- **Pilot**: 2 participants (1 expert, 1 general user)
- **Main study**: 2-3 sessions per day
- **Duration**: 2-3 weeks recruitment period

### Personnel
- **Facilitator**: Guides participant through study
- **Observer**: Takes notes, records data
- **Note**: Facilitator and observer can be same person

---

## 9. Pilot Study

### Pilot Goals
1. Test timing (is 90 minutes sufficient?)
2. Validate task difficulty
3. Check instruction clarity
4. Refine questionnaire

### Pilot Procedure
- Run full protocol with 2 participants
- Conduct debrief with research team
- Revise protocol based on feedback

### Success Criteria
- Both pilots complete within 90 minutes
- No critical usability issues
- Participants understand all tasks

---

## 10. Data Collection Sheet

```
Participant ID: ___
Date: ___
Group: [ ] Domain Expert [ ] Data Analyst [ ] General User
System Order: [ ] A-B-C [ ] A-C-B [ ] B-A-C [ ] B-C-A [ ] C-A-B [ ] C-B-A

TASK DATA:
| Task | System | Success | Time(s) | Attempts | Notes |
|------|--------|---------|---------|----------|-------|
| T1   |        | Y/N     |         |          |       |
| ...  |        |         |         |          |       |

QUESTIONNAIRE SCORES:
System A SUS: ___
System B SUS: ___
System C SUS: ___

Ranking: 1st: ___ 2nd: ___ 3rd: ___

INTERVIEW NOTES:
```

---

## Appendix A: Consent Form Template

[Standard IRB consent form including:
- Study purpose
- Procedures
- Risks and benefits
- Confidentiality
- Voluntary participation
- Contact information]

## Appendix B: SUS Questionnaire (Chinese)

1. 我认为我会愿意经常使用这个系统。
2. 我发现这个系统 unnecessarily complex。
3. 我认为这个系统容易使用。
4. 我认为我需要技术人员的支持才能使用这个系统。
5. 我发现这个系统的各种功能很好地整合在一起。
6. 我认为这个系统有太多不一致的地方。
7. 我会想象大多数人会很快学会使用这个系统。
8. 我发现这个系统非常 cumbersome 来使用。
9. 我感到非常有信心使用这个系统。
10. 我需要学习很多东西才能开始使用这个系统。

Scoring: Odd items (1,3,5,7,9): score - 1
        Even items (2,4,6,8,10): 5 - score
        Sum × 2.5 = SUS score (0-100)

## Appendix C: Task Scripts

[Detailed task descriptions and expected outputs]

---

**Protocol Version**: 1.0
**Date**: 2026-02-15
**Contact**: [Researcher Email]

# 📋 IEEE VIS 2026 Paper Improvement Plan

**Target Date:** March 31, 2026 | **Start Date:** March 5, 2026 | **Days Remaining:** 26

---

## Executive Summary

This plan guides the completion of the LAEV-Agents paper for IEEE VIS 2026 submission. The paper addresses domain-specific visualization using a multi-agent system with GraphRAG and iterative refinement.

**Current Status:**
- ✅ Technical implementation: 98.0% success rate
- ✅ Ablation study: Complete with 5 configurations
- ✅ Paper figures: 15+ generated
- ✅ Paper framework: LaTeX structure ready
- ❌ User study: Not started (BLOCKING)
- ❌ Related work: Needs 2024-2025 papers
- ❌ Direct LLM baseline: Quality uncertain

**Critical Path:** User study MUST be completed by March 20 to allow time for paper writing.

---

## Phase 1: Foundation & Preparation (Days 1-7, Mar 5-11)

### Week 1: March 5-11 (7 Days)

#### Day 1-2 (Mar 5-6): User Study Design

**Objective:** Complete user study protocol with 6-8 visualization tasks

**Deliverables:**
- `user_study/protocol.md` - Study design and procedure
- `user_study/tasks.pdf` - 6-8 task descriptions
- `user_study/sus_questionnaire.pdf` - SUS questionnaire
- `user_study/consent_form.pdf` - Consent form
- `user_study/data_collection.csv` - Data recording template

**Tasks:**

1. **Design 6-8 Visualization Tasks** (varying complexity):

| Task | Description | Expected Chart | Complexity |
|-------|-------------|----------------|--------------|
| T1 | Show total flights by aircraft type | Bar chart | Simple |
| T2 | Display monthly flight trend | Line chart | Simple |
| T3 | Compare weekend vs weekday flight patterns | Grouped bar | Medium |
| T4 | Show regional flight distribution | Map/heatmap | Medium |
| T5 | Analyze correlation between flight duration and distance | Scatter | Complex |
| T6 | Create dashboard showing flight metrics by district | Multi-panel | Complex |
| T7 | Find anomalies in flight patterns | Highlighted chart | Complex |
| T8 | Compare efficiency metrics across regions | Radar/combination | Complex |

2. **Create SUS Questionnaire** (standard 10 items, Likert 1-5):

```
1. I think that I would like to use this system frequently
2. I found the system unnecessarily complex
3. I thought the system was easy to use
4. I think that I would need the support of a technical person to be able to use this system
5. I found the various functions in this system were well integrated
6. I thought there was too much inconsistency in this system
7. I would imagine that most people would learn to use this system very quickly
8. I found the system very cumbersome to use
9. I felt very confident using the system
10. I needed to learn a lot of things before I could get going with this system
```

3. **Create Consent Form:**

Required elements:
- Purpose of study: Evaluating visualization system for LAE domain
- Time commitment: 30-40 minutes
- Data collection: SUS scores, task completion times, qualitative feedback
- Rights: Right to withdraw at any time
- Anonymity: All data will be anonymized and reported only in aggregate
- Contact: Researcher information

4. **Create Data Collection Template:**

```csv
participant_id,role_type,task_1_success,task_1_time,task_2_success,task_2_time,task_3_success,task_3_time,sus_1,sus_2,sus_3,sus_4,sus_5,sus_6,sus_7,sus_8,sus_9,sus_10,qualitative_notes
```

#### Day 3-4 (Mar 7-8): Investigate Direct LLM Baseline

**Objective:** Verify quality of Direct LLM baseline (100% success rate)

**Deliverables:**
- `user_study/baseline_analysis/direct_llm_review.md` - Review of 5 outputs
- `user_study/baseline_analysis/quality_comparison.pdf` - Side-by-side comparison
- `user_study/baseline_analysis/baseline_decision.md` - Final decision with rationale

**Tasks:**

1. **Select 5 diverse queries** from the 50 test queries:
   - Trend Analysis: TREND-01
   - Comparison: COMP-01
   - Distribution: DIST-01
   - Correlation: CORR-01
   - Exploration: EXPL-01

2. **Run Direct LLM baseline** on each query and capture:
   - Generated code
   - Execution success/failure
   - Screenshot of visualization
   - Time to generate

3. **Manually assess quality** of each output:
   - Chart type appropriateness
   - Data correctness
   - Visual elements (title, axis labels, legend)
   - Overall visual quality (1-5 scale)

4. **Compare with LAEV-Agents** on same queries:
   - Document quality differences
   - Note any systematic advantages

5. **Decision point:**
   - If Direct LLM produces high-quality visualizations → Keep as is
   - If Direct LLM produces low-quality visualizations → Document this limitation
   - Consider mentioning that Direct LLM "accepts syntactically correct but semantically questionable outputs"

#### Day 5-6 (Mar 9-10): Related Work Expansion

**Objective:** Add 10-15 recent papers (2024-2025) to Related Work section

**Deliverables:**
- `paper/bib/references.bib` - Updated with new references
- `paper/sections/related_work.md` - Updated with new paragraphs

**Tasks:**

1. **Search arXiv** for recent LLM+visualization papers:

```bash
# Search queries
site:arxiv.org "visualization" AND "LLM" (2024 OR 2025)
site:arxiv.org "natural language" AND "visualization" (2024 OR 2025)
site:arxiv.org "multi-agent" AND "code generation" (2024 OR 2025)
site:arxiv.org "retrieval" AND "visualization" (2024 OR 2025)
```

2. **Check IEEE VIS/TVCG 2024 proceedings** for:
   - LLM-based visualization papers
   - Multi-agent visualization systems
   - RAG-enhanced visualization work

3. **Select 10-15 papers** to add, prioritizing:
   - Publication year (2024-2025)
   - Venue (IEEE VIS, TVCG, CHI, IUI preferred)
   - Geographic/methodological diversity
   - Relevance to LLM+Vis, Multi-Agent, RAG+Vis

4. **For each paper, create entry:**
```bibtex
@article{Author2024Title,
  title = "Paper Title",
  author = "First Author and Second Author",
  journal = "Conference or Journal",
  year = {2024},
  note = {arXiv:xxxx.xxxxx}
}
```

5. **Update `paper/sections/related_work.md`** to:
   - Add new paragraph(s) for recent work
   - Update comparison table with new systems
   - Ensure proper citations

#### Day 7 (Mar 11): Recruit Participants

**Objective:** Confirm 4-6 participants for user study

**Deliverables:**
- `user_study/participants.csv` - Confirmed participant list
- `user_study/schedule.ics` - Calendar with sessions scheduled

**Tasks:**

1. **Recruit 2-3 domain experts:**
   - Target: UAV/LAE industry professionals
   - Channels: Colleagues, LinkedIn, professional networks
   - Incentive: ￥200 + lunch/coffee
   - Availability: Week 2 (Mar 12-18)

2. **Recruit 2-3 general users:**
   - Target: Data analysts or students
   - Channels: Campus, data analysis groups
   - Incentive: ￥100
   - Availability: Week 2 (Mar 12-18)

3. **Schedule sessions:**
   - Create calendar for Week 2 (Mar 12-18)
   - Each session: 30-40 minutes
   - Send confirmations with:
     - Date/time
     - Meeting link (Zoom/Tencent Meeting)
     - Consent form (pre-read)

**Participant targets:**
- Domain experts: 2-3 with UAV/LAE experience
- General users: 2-3 data analysis background
- Total: 4-6 participants

---

## Phase 2: User Study Execution (Days 8-14, Mar 12-18)

### Week 2: March 12-18 (7 Days)

#### Day 8-10 (Mar 12-14): Execute Domain Expert Sessions

**Participants:** 2-3 domain experts
**Time per session:** 30-40 minutes

**Session Protocol:**

| Time (min) | Activity | Notes |
|-------------|----------|-------|
| 0-5 | Introduction | Explain purpose, get consent signed |
| 5-10 | Task 1 | Participant reads task, attempts visualization |
| 10-15 | Task 2 | Participant attempts next visualization |
| 15-20 | Task 3 | Participant attempts final visualization |
| 20-25 | SUS Survey | Complete SUS questionnaire (10 items) |
| 25-35 | Debrief | Think-aloud feedback, ask open-ended questions |

**Data to Record:**
- Task success/failure for each of 3 tasks
- Completion time per task
- SUS scores (1-10)
- Qualitative observations (interesting quotes, confusion points)
- System used (if comparing multiple)

#### Day 11-13 (Mar 15-17): Execute General User Sessions

**Participants:** 2-3 general users
**Time per session:** 30-40 minutes
**Protocol:** Same as domain expert sessions

#### Day 14 (Mar 18): Data Consolidation

**Objective:** Analyze all user study data

**Deliverables:**
- `user_study/results/raw_data.csv` - All participant responses
- `user_study/results/sus_summary.pdf` - SUS statistics
- `user_study/results/task_completion_analysis.pdf` - Success rate by task type
- `user_study/results/qualitative_analysis.pdf` - Theme analysis
- `user_study/results/user_study_summary.md` - Key findings for paper

**Tasks:**

1. **Compile all user study data:**
   - Enter all SUS scores from all participants
   - Calculate average SUS score (target: ≥70)
   - Calculate standard deviation
   - Calculate task completion rate (overall and by complexity)
   - Calculate average completion time

2. **Statistical analysis:**
   - Compare domain experts vs general users (if sample size permits)
   - Calculate 95% confidence intervals
   - Perform paired t-test if comparing against baseline (optional)

3. **Identify qualitative themes:**
   - Common difficulties or confusions
   - Positive feedback highlights
   - Suggestions for improvement
   - Representative quotes

---

## Phase 3: Paper Writing (Days 15-21, Mar 19-25)

### Week 3: March 19-25 (7 Days)

#### Day 15-16 (Mar 19-20): Update Evaluation Section

**Deliverables:**
- `paper/sections/evaluation.tex` - Updated with user study
- `paper/figures/fig_user_study_results.pdf/png` - User study visualization

**Tasks:**

1. **Write user study subsection** including:
   - Participants (demographics, expertise level)
   - Procedure description (tasks, time allocation)
   - SUS results:
     - Mean and standard deviation
     - Interpretation (≥70 = good, <70 = needs work)
   - Task completion rates by complexity (simple/medium/complex)
   - Qualitative findings with representative quotes
   - Comparison of perceived usability vs system performance metrics

2. **Update evaluation section structure:**
```latex
\section{Evaluation}
\subsection{Experimental Setup}
  - Dataset and queries (50 queries, 6 task types)
  - Baselines (NL4DV, Direct LLM)
  - Evaluation metrics (success rate, quality score, time)

\subsection{Quantitative Results}
  - Success rate comparison (Table X)
  - Performance analysis (Figure X)
  - Task-type breakdown (Figure X)
  - Ablation study (Table X, Figure X)

\subsection{User Study}
  - Participants and protocol
  - SUS scores and interpretation
  - Task completion analysis
  - Qualitative findings

\subsection{Quality Analysis}
  - Quality scores by system (Figure X)
  - Iterative refinement impact
  - Failure case analysis
```

3. **Create user study figures:**
   - SUS score distribution (box plot or histogram)
   - Task completion rate by type (bar chart)
   - Comparison of domain experts vs general users (if data permits)

#### Day 17-18 (Mar 21-22): Write Method Section

**Deliverables:**
- `paper/sections/method.tex` - Complete with pseudocode
- `paper/figures/fig_design_space.pdf/png` - Design space visualization
- `paper/figures/fig_agent_workflow.pdf/png` - Agent workflow diagram

**Tasks:**

1. **Add algorithm pseudocode for the multi-agent pipeline**

2. **Formalize design space:**
   - Define task types: $\mathcal{T} = \{\text{trend}, \text{compare}, \text{distribution}\}$
   - Define data characteristics: $\mathcal{D} = \{\text{temporal}, \text{categorical}, \text{geospatial}\}$
   - Define chart types: $\mathcal{C} = \{\text{bar}, \text{line}, \text{scatter}\}$
   - Design space: $\mathcal{S} = \mathcal{T} \times \mathcal{D} \times \mathcal{C}$
   - Show mapping: $\mathcal{M}: \mathcal{S} \rightarrow \mathcal{C}$

3. **Describe agent responsibilities in detail:**
   - Planner: Intent analysis, task decomposition, complexity assessment
   - Retriever: GraphRAG query formulation, context extraction
   - Coder: Code generation strategies (adaptive/conservative)
   - Evaluator: Multi-dimensional quality assessment (readability, aesthetics, data encoding, domain appropriateness)
   - Reflector: Error analysis, refinement triggers

#### Day 19-20 (Mar 23-24): Update Introduction & Discussion

**Deliverables:**
- `paper/sections/introduction.md` - Updated and polished
- `paper/sections/discussion.md` - Complete with limitations and future work
- `paper/tex/main.tex` - Updated with new sections

**Tasks:**

1. **Enhance Introduction:**
   - Add concrete examples of LAE visualization challenges
   - Strengthen motivation with specific domain pain points
   - Sharpen contribution statement with quantified claims:
     - "We improve success rate by X% over NL4DV"
     - "Our GraphRAG adds 130 domain entities"
     - "Iterative refinement recovers Y% of failures"
   - Update abstract with user study results (when available)
   - Update abstract: Change "32" to "50" queries

2. **Write Discussion section:**
   - **Limitations:**
     1. Domain-specificity to low-altitude economy
     2. Knowledge graph requires manual construction effort
     3. LLM API dependency (cost, reliability)
     4. 2% failure cases still require explanation
     5. Scalability to very large knowledge graphs
   - **Future work:**
     1. Automated knowledge graph construction from documents
     2. Multi-domain adaptation and transfer learning
     3. Integration with more visualization libraries (Vega, D3.js)
     4. Real-time collaborative visualization
     5. User study with larger sample size and controlled experiment

#### Day 21 (Mar 25): Failure Case Analysis

**Deliverables:**
- `paper/sections/evaluation.tex` - Add failure analysis subsection
- `paper/figures/fig_failure_analysis.pdf/png` - Failure types visualization

**Tasks:**

1. **Identify and categorize all 1-2 failures** from 50 queries:
   - Semantic understanding failures (misinterpreted intent)
   - Retrieval failures (couldn't find relevant context)
   - Code generation failures (syntax errors, wrong chart type)
   - Quality failures (passed evaluation but visually wrong)

2. **For each category:**
   - Count occurrences
   - Provide representative example
   - Explain root cause
   - Document whether Reflector could/couldn't fix it

3. **Create failure analysis visualizations:**
   - Pie chart of failure types
   - Sankey diagram showing where failures occur in pipeline

---

## Phase 4: Internal Review (Days 22-25, Mar 26-29)

### Week 4: March 26-29 (4 Days)

#### Day 22-23 (Mar 26-27): First Internal Review

**Reviewers:** 2-3 colleagues (including yourself)

**Review Checklist:**

**Technical Accuracy:**
- [ ] Are all results correct?
- [ ] Are comparisons fair to baselines?
- [ ] Are claims supported by data?
- [ ] Are statistics properly computed?

**Logical Flow:**
- [ ] Does Introduction motivate the work clearly?
- [ ] Does Related Work establish proper context?
- [ ] Is contribution clear and novel?
- [ ] Do results support claims made?
- [ ] Is Discussion grounded in results?

**Writing Quality:**
- [ ] Is language clear and concise?
- [ ] Are there grammatical errors?
- [ ] Are figures/tables properly referenced?
- [ ] Is notation consistent throughout?

**Completeness:**
- [ ] Are all sections present?
- [ ] Are all necessary figures included?
- [ ] Is supplementary material prepared?

**Process:**
1. Each reviewer reads independently
2. Compile feedback in `paper/review_feedback_round1.md`
3. Prioritize issues: Critical > High > Low
4. Address critical and high-priority issues

#### Day 24-25 (Mar 28-29): Address Feedback & Supplemental

**Deliverables:**
- `paper/sections/*` - Updated based on feedback
- `supplemental/` - Complete supplemental materials package

**Tasks:**

1. **Address review feedback:**
   - Fix critical issues immediately
   - Address high-priority concerns
   - Note low-priority issues for post-decision

2. **Create supplemental materials:**

```
supplemental/
├── test_queries.json             # All 50 queries with metadata
├── example_outputs/
│   ├── successful/              # 5-10 best visualizations
│   ├── failures/                 # Representative failures
│   └── refinements/              # 2-3 iteration examples
├── user_study_materials/
│   ├── protocol.pdf
│   ├── sus_questionnaire.pdf
│   ├── consent_form.pdf
│   └── results_summary.pdf
├── data/
│   ├── sample_flight_data.csv  # Sample dataset
│   └── knowledge_graph.json       # Entity/relationship schema
├── setup/
│   ├── docker-compose_setup.md     # Docker setup instructions
│   ├── installation_guide.md        # Full installation
│   └── requirements.txt             # Python dependencies
└── README.md                       # Supplemental index
```

3. **Update main.tex:**
   - Add reference to supplemental material
   - Ensure all figures/tables properly numbered
   - Check cross-references

---

## Phase 5: Final Polish & Submission (Days 26-28, Mar 30 - Apr 1)

### Week 5: March 30 - April 1 (3 Days)

#### Day 26 (Mar 30): Anonymization & Formatting

**Deliverables:**
- `paper/paper.pdf` - Final anonymous PDF
- `paper/paper_checklist.pdf` - Format verification

**Tasks:**

1. **Anonymization check:**
   - [ ] Remove all author names from LaTeX
   - [ ] Remove all institution information
   - [ ] Remove project-specific URLs
   - [ ] Remove acknowledgments (add placeholder for post-review)
   - [ ] Check for any identifying metadata in PDF

2. **Format compliance:**
   - [ ] Check IEEE VIS template requirements
   - [ ] Verify page count (≤10 pages for TVCG, check guidelines)
   - [ ] Verify font sizes (≥9pt for body text)
   - [ ] Verify figure quality (≥300 DPI)
   - [ ] Check figure captions and numbering

3. **Generate final PDF:**
```bash
cd paper/tex
xelatex -interaction=nonstopmode main.tex
```

4. **Validate PDF:**
   - Check for formatting issues
   - Verify no author info in metadata
   - Check file size (within limits)
   - Ensure all figures/tables render correctly

#### Day 27 (Apr 1): Final Review & Submit

**Tasks:**

1. **Final submission checklist:**
   - [ ] All sections complete and written
   - [ ] All figures/tables present and numbered
   - [ ] All references cited and formatted
   - [ ] No author identification
   - [ ] File size within submission limits
   - [ ] PDF generated successfully
   - [ ] Supplemental material ready (if needed)

2. **Submit to IEEE VIS 2026:**
   - Go to PCS (Paper Submission System)
   - Complete submission form
   - Upload paper.pdf
   - Upload supplemental materials (if any)
   - Confirm submission
   - ✅ **SUBMITTED**

---

## Daily Task Schedule (26 Days)

| Day | Date | Primary Focus | Key Deliverable |
|-----|-------|---------------|-----------------|
| 1 | Mar 5 | User study design - Tasks | Design 6-8 tasks |
| 2 | Mar 6 | User study design - Forms | SUS questionnaire, consent form |
| 3 | Mar 7 | Direct LLM review - Part 1 | Review 2-3 outputs |
| 4 | Mar 8 | Direct LLM review - Part 2 | Review remaining, decision |
| 5 | Mar 9 | Related work - Search | Query arXiv, find papers |
| 6 | Mar 10 | Related work - Update | Add papers to related_work.md |
| 7 | Mar 11 | Participant recruitment | 4-6 confirmed participants |
| 8 | Mar 12 | User study - Domain experts | 2 expert sessions |
| 9 | Mar 13 | User study - Domain experts | Complete expert sessions |
| 10 | Mar 14 | User study - General users | 2 general user sessions |
| 11 | Mar 15 | User study - General users | Complete sessions, data |
| 12 | Mar 16 | User study - Analysis | SUS summary, statistics |
| 13 | Mar 17 | User study - Analysis | Task completion, qualitative |
| 14 | Mar 18 | User study - Complete | user_study_summary.md |
| 15 | Mar 19 | Paper - Evaluation section | evaluation.tex with user study |
| 16 | Mar 20 | Paper - Evaluation figures | User study figures |
| 17 | Mar 21 | Paper - Method section | method.tex with pseudocode |
| 18 | Mar 22 | Paper - Method figures | Design space, workflow figures |
| 19 | Mar 23 | Paper - Introduction | Update introduction.md |
| 20 | Mar 24 | Paper - Discussion | discussion.md |
| 21 | Mar 25 | Paper - Failure analysis | Failure analysis section + figure |
| 22 | Mar 26 | Review - Round 1 | review_feedback_round1.md |
| 23 | Mar 27 | Review - Address feedback | Update sections |
| 24 | Mar 28 | Supplemental | Create supplemental package |
| 25 | Mar 29 | Supplemental | Complete main.tex updates |
| 26 | Mar 30 | Final - Anonymize | paper.pdf (anonymous) |
| 27 | Apr 1 | Final - Submit | ✅ SUBMITTED |

---

## Critical Milestones

| Milestone | Date | Success Criteria |
|-----------|-------|-----------------|
| User study protocol ready | Mar 6 | 8 tasks, SUS, consent form designed |
| Participants recruited | Mar 11 | 4-6 participants confirmed |
| Baseline verified | Mar 8 | Direct LLM quality confirmed |
| Related work updated | Mar 10 | 10+ 2024-2025 papers added |
| User study complete | Mar 18 | All sessions done, data analyzed |
| Evaluation section written | Mar 20 | User study results integrated |
| Method section written | Mar 22 | Pseudocode added |
| Paper first draft done | Mar 25 | All sections written |
| Internal review done | Mar 29 | Feedback addressed |
| Paper finalized | Mar 30 | Anonymous PDF ready |
| **SUBMITTED** | Apr 1 | ✅ |

---

## Risk Management

| Risk | Probability | Impact | Mitigation |
|-------|-------------|---------|------------|
| User recruitment fails | Medium | High | Use colleagues, offer higher incentive |
| Participants drop out | Medium | Medium | Overschedule by 20% |
| Baseline quality issues | Low | High | Investigate Day 3-4, document findings |
| Related work insufficient | Low | Medium | Dedicate 2 full days to search |
| Writing falls behind | Medium | High | Prioritize sections, cut features |
| Technical issues with submission | Low | Critical | Test submission system early |

---

## Resource Requirements

| Resource | Required | Available | Action |
|-----------|-----------|-----------|--------|
| Domain experts | 2-3 | Yes | Recruit by Mar 11 |
| General users | 2-3 | Yes | Recruit by Mar 11 |
| Participant incentives | ￥800-1600 | Yes | Budget approved |
| Internal reviewers | 2-3 | Yes | Colleagues available |
| arXiv access | Yes | Yes | Free |
| Submission system | PCS account | ? | Create if needed |

---

## Success Metrics

**Pre-submission (by Mar 30):**
- [ ] User study: SUS score ≥ 70
- [ ] User study: ≥ 8 participants
- [ ] Related work: ≥ 10 recent papers (2024-2025)
- [ ] Baseline: Direct LLM quality verified
- [ ] Paper: All sections written
- [ ] Paper: ≥ 10 figures included
- [ ] Review: Internal review completed

**Post-submission:**
- [ ] Accepted ✅
- [ ] Rejected with useful feedback

---

## Files to Create (Complete List)

### User Study
```
user_study/
├── protocol.md              # Study design and procedure
├── tasks.pdf               # 6-8 task descriptions
├── sus_questionnaire.pdf   # SUS questionnaire
├── consent_form.pdf         # Consent form
├── data_collection.csv       # Data recording template
├── participants.csv          # Confirmed participants
├── schedule.ics              # Session calendar
├── baseline_analysis/
│   ├── direct_llm_review.md
│   ├── quality_comparison.pdf
│   └── baseline_decision.md
└── results/
    ├── raw_data.csv
    ├── sus_summary.pdf
    ├── task_completion_analysis.pdf
    ├── qualitative_analysis.pdf
    └── user_study_summary.md
```

### Paper
```
paper/
├── sections/
│   ├── related_work.md       # Updated with recent papers
│   ├── evaluation.tex          # Updated with user study
│   ├── method.tex             # With pseudocode
│   ├── introduction.md         # Updated and polished
│   ├── discussion.md           # With limitations/future work
│   └── design_space.tex        # Design space formalization
├── figures/
│   ├── fig_user_study_results.pdf/png
│   ├── fig_user_study_sus_distribution.pdf/png
│   ├── fig_design_space.pdf/png
│   ├── fig_agent_workflow.pdf/png
│   └── fig_failure_analysis.pdf/png
├── bib/
│   └── references.bib           # Updated
└── tex/
    ├── main.tex                 # Finalized
    └── review_checklist.pdf     # Format verification
```

### Review
```
paper/
├── review_feedback_round1.md  # Collected feedback
├── review_checklist.md        # Review checklist
└── anonymization_report.md    # Anonymization notes
```

### Supplemental
```
supplemental/
├── test_queries.json
├── example_outputs/
│   ├── successful/
│   ├── failures/
│   └── refinements/
├── user_study_materials/
│   ├── protocol.pdf
│   ├── sus_questionnaire.pdf
│   ├── consent_form.pdf
│   └── results_summary.pdf
├── data/
│   ├── sample_flight_data.csv
│   └── knowledge_graph.json
├── setup/
│   ├── docker-compose_setup.md
│   ├── installation_guide.md
│   └── requirements.txt
└── README.md
```

---

**Last Updated:** March 5, 2026
**Status:** Ready to execute

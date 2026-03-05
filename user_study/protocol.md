# LAEV-Agents User Study Protocol

**Study Title:** Evaluation of LAEV-Agents for Domain-Specific Data Visualization

**Study Period:** March 12-18, 2026
**Study Type:** Remote, individual sessions via video conference
**Target Participants:** 4-6 (2-3 domain experts + 2-3 general users)

---

## Study Objectives

1. **Primary Objective:** Evaluate the usability and effectiveness of LAEV-Agents for generating domain-specific visualizations in the low-altitude economy context.

2. **Secondary Objectives:**
   - Compare task completion success between different complexity levels
   - Assess user satisfaction through SUS (System Usability Scale) questionnaire
   - Identify strengths and weaknesses of the current system
   - Collect qualitative feedback for system improvement

---

## Participants

### Participant Profiles

| Category | Target | Characteristics |
|-----------|--------|-----------------|
| Domain Experts | 2-3 | UAV/LAE industry professionals with 1+ years experience |
| General Users | 2-3 | Data analysts or students with experience in data visualization tools |
| **Total** | **4-6** | **Target** |

### Inclusion Criteria

**Domain Experts:**
- Professional experience in UAV/LAE domain
- Familiarity with data analysis or visualization
- Available for 30-40 minute remote session
- Comfortable with video conferencing

**General Users:**
- Experience with data analysis or visualization (Tableau, Power BI, etc.)
- No specific UAV/LAE domain knowledge required
- Available for 30-40 minute remote session
- Comfortable with video conferencing

### Exclusion Criteria

- Current or former contributors to LAEV-Agents project
- Have participated in similar studies in the past 3 months
- Visual or hearing impairments that prevent use of the system

---

## Study Tasks

Participants will complete **8 visualization tasks** of varying complexity.

### Task Descriptions

#### Simple Tasks (T1-T2)

**T1: Aircraft Type Distribution**
> "Show me a bar chart displaying the total number of flights by aircraft type (e.g., MultiRotor, FixedWing, Helicopter). Use different colors for each aircraft type and include a chart title and axis labels."

**Expected Output:** Bar chart showing flight counts by aircraft type

**Success Criteria:**
- Correct chart type (bar chart)
- Correct data (grouped by aircraft type)
- Proper labels (chart title, x-axis label, y-axis label)
- Correct colors (distinct for each category)

---

**T2: Monthly Flight Trend**
> "Create a line chart that shows the trend of flight operations over time. Display the total number of flights for each month from January to December. Include a chart title and label the x-axis with months."

**Expected Output:** Line chart showing monthly flight trend

**Success Criteria:**
- Correct chart type (line chart)
- Correct temporal data (x-axis: months, y-axis: flight counts)
- Proper labels (chart title, axis labels)
- Data points correctly ordered chronologically

---

#### Medium Tasks (T3-T4)

**T3: Weekend vs Weekday Comparison**
> "Compare flight patterns between weekends and weekdays. Show me a grouped bar chart where weekends and weekdays are shown side by side for each aircraft type. Include a legend to distinguish weekend vs weekday."

**Expected Output:** Grouped bar chart comparing weekend vs weekday by aircraft type

**Success Criteria:**
- Correct chart type (grouped bar chart)
- Correct grouping (weekend vs weekday)
- Correct data aggregation (counts for each group)
- Proper legend to distinguish groups
- Proper labels

---

**T4: Regional Flight Distribution**
> "Display the geographic distribution of flights across different districts. Show me a map or heatmap where regions are colored based on flight density. Include a color legend to indicate the number of flights."

**Expected Output:** Map or heatmap showing flight distribution by region

**Success Criteria:**
- Correct chart type (map or heatmap)
- Correct geographic mapping
- Color scale represents flight density
- Proper legend included
- Title and labels present

---

#### Complex Tasks (T5-T8)

**T5: Duration vs Distance Correlation**
> "Analyze the relationship between flight duration and flight distance. Create a scatter plot where each point represents a flight, with duration on the y-axis and distance on the x-axis. Look for any patterns or trends."

**Expected Output:** Scatter plot showing correlation between duration and distance

**Success Criteria:**
- Correct chart type (scatter plot)
- Correct axes (x-axis: distance, y-axis: duration)
- Data points correctly plotted
- Title and axis labels present
- Trend line or correlation analysis (optional but good)

---

**T6: Comprehensive Metrics Dashboard**
> "Create a multi-panel dashboard that shows key flight metrics for different districts. Include at least 3 different visualizations: (1) total flights by district, (2) average duration by district, and (3) aircraft type distribution by district. Use appropriate chart types for each visualization."

**Expected Output:** Multi-panel dashboard with 3+ visualizations

**Success Criteria:**
- Multiple chart types included
- Each chart shows different metric
- Data correctly aggregated by district
- Proper layout (panels arranged logically)
- Titles and labels for each panel

---

**T7: Anomaly Detection**
> "Find flights with unusual patterns. Create a visualization that highlights flights that are significantly different from others. For example, flights that are much longer than average for their distance, or flights that occurred at unusual times."

**Expected Output:** Visualization highlighting anomalies (e.g., scatter plot with highlighted points, or chart with threshold lines)

**Success Criteria:**
- Correct identification of anomalies (clearly distinguished from normal data)
- Appropriate method for highlighting (color, marker, or threshold)
- Context provided (why these are anomalies)
- Title and labels present

---

**T8: Multi-dimensional Efficiency Comparison**
> "Compare efficiency metrics across different regions using a radar chart or combination chart. Include metrics such as average duration, success rate, and operational efficiency for at least 4 different districts."

**Expected Output:** Radar or combination chart comparing multiple dimensions across regions

**Success Criteria:**
- Appropriate chart type (radar or combination)
- Multiple metrics compared (at least 3)
- Multiple regions compared (at least 4)
- Data correctly aggregated
- Legend included (if radar chart)
- Title and labels present

---

## Session Protocol

Each participant session will follow this structure:

### 1. Introduction (5 minutes)

**Facilitator Script:**
```
"Thank you for participating in this user study. My name is [Your Name] and I'm a researcher studying tools for data visualization in the low-altitude economy domain.

The purpose of this study is to evaluate a new system called LAEV-Agents that helps users create visualizations through natural language. Your feedback will help us understand how to improve such systems.

During this session, you will:
1. Attempt to create 8 different visualizations using the system
2. Complete a short questionnaire about your experience
3. Provide feedback through think-aloud comments

The session will take approximately 30-40 minutes.

Before we begin, please read and sign this consent form, which explains your rights and how your data will be used."
```

### 2. Consent Form (3 minutes)

Participants read and sign the consent form (`user_study/consent_form.pdf`).

### 3. System Tutorial (5 minutes)

Brief demonstration of LAEV-Agents interface:
- How to enter a query
- How to interpret the generated visualization
- How to use basic controls (regenerate, modify)

### 4. Task Completion (15 minutes)

Participants attempt the 8 tasks in order (T1-T8). For each task:
- Read the task description
- Enter the query into the system
- Evaluate the generated visualization
- Mark success/failure
- If failed, may try up to 2 additional attempts

**Data Recorded:**
- Task success (yes/no)
- Number of attempts
- Completion time per task

### 5. SUS Questionnaire (5 minutes)

Participants complete the 10-item SUS questionnaire (`user_study/sus_questionnaire.pdf`).

### 6. Debrief (5-10 minutes)

Open-ended feedback questions:
1. "What did you like most about the system?"
2. "What did you find most difficult or frustrating?"
3. "How would you compare this system to other tools you've used for visualization?"
4. "What features would you add or change?"
5. "Any other comments or suggestions?"

---

## Data Collection

### Data Recording Template

All session data will be recorded in `user_study/results/raw_data.csv`:

```csv
participant_id,participant_type,date,time_slot,task_1_success,task_1_attempts,task_1_time,task_2_success,task_2_attempts,task_2_time,task_3_success,task_3_attempts,task_3_time,task_4_success,task_4_attempts,task_4_time,task_5_success,task_5_attempts,task_5_time,task_6_success,task_6_attempts,task_6_time,task_7_success,task_7_attempts,task_7_time,task_8_success,task_8_attempts,task_8_time,sus_1,sus_2,sus_3,sus_4,sus_5,sus_6,sus_7,sus_8,sus_9,sus_10,qualitative_notes
```

### Data Types

- `participant_id`: Unique identifier (e.g., P001, P002, ...)
- `participant_type`: "domain_expert" or "general_user"
- `date`: Session date
- `time_slot`: Session time (e.g., "morning", "afternoon")
- `task_X_success`: Boolean indicating task completion success
- `task_X_attempts`: Number of attempts before success or giving up
- `task_X_time`: Time in seconds to complete task
- `sus_X`: SUS item score (1-5 Likert scale)
- `qualitative_notes`: Free-text feedback from debrief

---

## Success Criteria

### Task Success Criteria

A task is considered "successful" if:
1. **Correct chart type** is generated (matches task requirements)
2. **Data is correctly encoded** (correct aggregation, proper data mapping)
3. **Essential elements are present** (title, axis labels, legend as needed)
4. **Visualization is meaningful** (not syntactically correct but semantically wrong)

A task is considered "failed" if:
- Participant gives up after 2 unsuccessful attempts
- Generated visualization is syntactically incorrect
- System produces an error or fails to respond

### Overall Success Rate

Calculate success rate as:
```
Success Rate = (Successful Tasks / Total Tasks Attempted) × 100%
```

### SUS Score Interpretation

SUS scores range from 10 to 50:
- **Excellent (≥70):** System has high usability
- **Good (55-69):** Good but can be improved
- **OK (40-54):** Marginal usability
- **Poor (<40):** Low usability, needs significant improvement

Target: Average SUS score ≥ 70 for acceptance.

---

## Ethical Considerations

1. **Informed Consent:** All participants provide written informed consent
2. **Anonymity:** All participant data will be anonymized; only aggregate results will be reported
3. **Right to Withdraw:** Participants may withdraw at any time without penalty
4. **Data Security:** Raw data will be stored securely and only accessible to researchers
5. **Minimal Risk:** No physical or psychological risks beyond normal computer usage

---

## Timeline

| Week | Dates | Activity |
|-------|--------|-----------|
| Week 1 | Mar 5-11 | Protocol design, participant recruitment |
| Week 2 | Mar 12-18 | User study execution (all sessions) |
| Week 3 | Mar 19-25 | Data analysis, paper integration |

---

## Contact Information

**Primary Researcher:** [Your Name]
**Email:** [your.email@institution.edu]
**Study Dates:** March 12-18, 2026
**Platform:** Zoom/Tencent Meeting (link will be provided)

---

## References

1. Brooke, J. (1986). SUS: A quick and dirty usability scale. Usability Evaluation in Industry.
2. Lewis, J. R. (1995). IBM Computer Usability Satisfaction Questionnaires: Psychometric Evaluation of Other Versions.

---

**Version:** 1.0
**Last Updated:** March 5, 2026

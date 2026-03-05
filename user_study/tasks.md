# LAEV-Agents User Study Tasks

**Study Date:** March 12-18, 2026
**Number of Tasks:** 8
**Estimated Time:** 30-40 minutes total

---

## Task Descriptions

### Task 1: Aircraft Type Distribution (Simple)

**Query to Enter:**
> "Show me a bar chart displaying the total number of flights by aircraft type (e.g., MultiRotor, FixedWing, Helicopter). Use different colors for each aircraft type and include a chart title and axis labels."

**Expected Output:**
- A bar chart showing flight counts by aircraft type
- Distinct colors for each aircraft type
- Chart title: "Total Flights by Aircraft Type"
- X-axis label: "Aircraft Type"
- Y-axis label: "Number of Flights"

**Example of Successful Output:**
A bar chart with 3-5 bars (one per aircraft type), each bar in a different color, with a clear title and properly labeled axes.

---

### Task 2: Monthly Flight Trend (Simple)

**Query to Enter:**
> "Create a line chart that shows the trend of flight operations over time. Display the total number of flights for each month from January to December. Include a chart title and label the x-axis with months."

**Expected Output:**
- A line chart showing monthly flight trend
- X-axis: Month names (January, February, ..., December)
- Y-axis: Total number of flights
- Chart title: "Monthly Flight Trend"
- X-axis label: "Month"
- Y-axis label: "Number of Flights"

**Example of Successful Output:**
A line chart with 12 data points, showing upward or seasonal trends, with all elements properly labeled.

---

### Task 3: Weekend vs Weekday Comparison (Medium)

**Query to Enter:**
> "Compare flight patterns between weekends and weekdays. Show me a grouped bar chart where weekends and weekdays are shown side by side for each aircraft type. Include a legend to distinguish weekend vs weekday."

**Expected Output:**
- A grouped bar chart
- Aircraft types on the x-axis
- Two bars per aircraft type (weekend, weekday)
- Legend distinguishing weekend vs weekday
- Chart title: "Weekend vs Weekday Flight Patterns by Aircraft Type"
- Y-axis label: "Number of Flights"

**Example of Successful Output:**
A grouped bar chart with 3 aircraft types, each showing two bars (weekend and weekday), clearly labeled with a legend.

---

### Task 4: Regional Flight Distribution (Medium)

**Query to Enter:**
> "Display the geographic distribution of flights across different districts. Show me a map or heatmap where regions are colored based on flight density. Include a color legend to indicate the number of flights."

**Expected Output:**
- A map or heatmap showing flight distribution by region
- Color scale representing flight density (e.g., light green = low, dark red = high)
- Color legend showing the flight count range
- Chart title: "Regional Flight Distribution"
- Region labels visible

**Example of Successful Output:**
A heatmap with districts labeled, color-coded by flight density, with a legend showing "0-100 flights", "100-200 flights", etc.

---

### Task 5: Duration vs Distance Correlation (Complex)

**Query to Enter:**
> "Analyze the relationship between flight duration and flight distance. Create a scatter plot where each point represents a flight, with duration on the y-axis and distance on the x-axis. Look for any patterns or trends."

**Expected Output:**
- A scatter plot
- X-axis: Flight Distance (km)
- Y-axis: Flight Duration (minutes)
- Data points scattered to show correlation
- Optional: Trend line showing relationship
- Chart title: "Flight Duration vs Distance Correlation"
- Axis labels present

**Example of Successful Output:**
A scatter plot with many data points, potentially showing a positive correlation (longer flights tend to cover more distance), with axes and title properly labeled.

---

### Task 6: Comprehensive Metrics Dashboard (Complex)

**Query to Enter:**
> "Create a multi-panel dashboard that shows key flight metrics for different districts. Include at least 3 different visualizations: (1) total flights by district, (2) average duration by district, and (3) aircraft type distribution by district. Use appropriate chart types for each visualization."

**Expected Output:**
- Multiple charts/panels (at least 3)
- Each chart shows a different metric
- All charts use district as the grouping dimension
- Appropriate chart types for each metric:
  - (1) Bar chart for total flights
  - (2) Bar or radar chart for average duration
  - (3) Stacked bar or pie chart for aircraft type distribution
- Proper layout (panels arranged logically)
- Titles and labels for each panel

**Example of Successful Output:**
A dashboard with 3 panels:
- Panel 1: Bar chart showing total flights per district
- Panel 2: Bar chart showing average flight duration per district
- Panel 3: Stacked bar chart showing aircraft type distribution per district

---

### Task 7: Anomaly Detection (Complex)

**Query to Enter:**
> "Find flights with unusual patterns. Create a visualization that highlights flights that are significantly different from others. For example, flights that are much longer than average for their distance, or flights that occurred at unusual times."

**Expected Output:**
- A visualization that highlights anomalies
- Options: scatter plot with highlighted points, box plot with outliers marked, or chart with threshold lines
- Clear indication of what makes a data point anomalous (e.g., "duration > 2× average")
- Context provided (why these are anomalies)
- Chart title: "Anomalous Flight Patterns"
- Labels explaining the anomaly criteria

**Example of Successful Output:**
A scatter plot with most data points in one color, and anomalous points highlighted in red (e.g., "Flights with duration > 60 minutes"), with a legend or annotation explaining the criteria.

---

### Task 8: Multi-dimensional Efficiency Comparison (Complex)

**Query to Enter:**
> "Compare efficiency metrics across different regions using a radar chart or combination chart. Include metrics such as average duration, success rate, and operational efficiency for at least 4 different districts."

**Expected Output:**
- A radar or combination chart
- At least 4 regions compared
- At least 3 different metrics (dimensions)
- Each metric properly scaled and normalized
- Legend included (if radar chart)
- Chart title: "Multi-dimensional Efficiency Comparison by District"
- Axis/legend labels clearly identifying metrics

**Example of Successful Output:**
A radar chart with 4 axes (one per metric), with 4 polygons (one per district), showing how each district performs across the different efficiency metrics, with a legend.

---

## Task Order and Time Allocation

Participants will attempt tasks in order: T1 → T2 → T3 → T4 → T5 → T6 → T7 → T8

| Task | Complexity | Estimated Time |
|-------|-----------|---------------|
| T1 | Simple | 2 minutes |
| T2 | Simple | 2 minutes |
| T3 | Medium | 3 minutes |
| T4 | Medium | 3 minutes |
| T5 | Complex | 2 minutes |
| T6 | Complex | 2 minutes |
| T7 | Complex | 2 minutes |
| T8 | Complex | 3 minutes |
| **Total** | - | **19 minutes** |

Note: This leaves ~11 minutes for introduction (5), tutorial (5), SUS (5), and debrief (5-10).

---

## Evaluation Criteria

For each task, the evaluator (researcher) will mark:

| Criterion | Description | Score (1-5) |
|-----------|-------------|---------------|
| Chart Type | Correct type of visualization generated | 1-5 |
| Data Accuracy | Data correctly encoded and aggregated | 1-5 |
| Labels | Title, axes, legend present and correct | 1-5 |
| Visual Quality | Clear, readable, aesthetically pleasing | 1-5 |

A task is **successful** if average score ≥ 3.5.

---

## Notes for Participants

1. **Don't rush:** Take your time to read each task carefully
2. **Read the query exactly as written:** Enter it word-for-word into the system
3. **Evaluate the output:** Does it match what you expected?
4. **If it fails:** Try once more with the same query
5. **If still fails:** Move to the next task
6. **Be honest:** Your feedback helps us improve the system

---

## Version History

- v1.0: Initial version created March 5, 2026

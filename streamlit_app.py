import streamlit as st
from streamlit_echarts import st_pyecharts
import data_factory
import charts_lib

st.set_page_config(page_title="Low Altitude Economy Index", layout="wide")

st.title("Low Altitude Economy Development Index")
st.markdown("### White Paper 2024 Dashboard")

# Load Data
data = data_factory.generate_data()

# ----------------- Dashboard Overview -----------------
st.divider()
col1, col2 = st.columns([1, 3])
with col1:
    st_pyecharts(charts_lib.dashboard_chart(data["dashboard"]), height="300px")
with col2:
    st.markdown("""
    **Executive Summary**

    The index is calculated based on a 5-Dimension framework:
    - **Scale**: Market size and growth.
    - **Structure**: Fleet and entity composition.
    - **Space**: Regional balance and airspace usage.
    - **Efficiency**: Operational quality and endurance.
    - **Innovation**: Tech leadership and new integration.
    """)

# ----------------- 1. Scale & Growth -----------------
st.header("1. Scale & Growth")
col1, col2 = st.columns(2)
with col1:
    st_pyecharts(charts_lib.traffic_area_chart(data["traffic"]), height="400px")
with col2:
    st_pyecharts(charts_lib.operation_dual_line(data["operation"]), height="400px")

# ----------------- 2. Structure & Entity -----------------
st.header("2. Structure & Entity")
c1, c2, c3 = st.columns(3)
with c1:
    st_pyecharts(charts_lib.fleet_stacked_bar(data["fleet"]), height="350px")
with c2:
    st_pyecharts(charts_lib.pareto_chart(data["pareto"]), height="350px")
with c3:
    st_pyecharts(charts_lib.rose_chart(data["rose"]), height="350px")

st_pyecharts(charts_lib.treemap_chart(data["treemap"]), height="400px")

# ----------------- 3. Time & Space -----------------
st.header("3. Time & Space")
c1, c2 = st.columns([2, 1])
with c1:
    st.subheader("Regional Heatmap")
    st_pyecharts(charts_lib.map_chart(data["map"]), height="500px")
with c2:
    st_pyecharts(charts_lib.polar_clock_chart(data["polar"]), height="500px")

st.subheader("Calendar Activity")
st_pyecharts(charts_lib.calendar_heatmap(data["calendar"]), height="250px")

c1, c2 = st.columns(2)
with c1:
    st_pyecharts(charts_lib.night_wave_chart(data["night"]), height="300px")
with c2:
    st_pyecharts(charts_lib.chord_chart(data["chord"]), height="400px") # Micro circulation often spatial

# ----------------- 4. Efficiency & Quality -----------------
st.header("4. Efficiency & Quality")
c1, c2, c3 = st.columns(3)
with c1:
    st_pyecharts(charts_lib.seasonal_boxplot(data["seasonal"]), height="350px")
with c2:
    st_pyecharts(charts_lib.gauge_chart(data["gauge"]), height="350px")
with c3:
    st_pyecharts(charts_lib.funnel_chart(data["funnel"]), height="350px")

st_pyecharts(charts_lib.histogram_chart(data["histogram"]), height="300px")

# ----------------- 5. Innovation & Integration -----------------
st.header("5. Innovation & Integration")
c1, c2 = st.columns(2)
with c1:
    st_pyecharts(charts_lib.radar_chart(data["radar"]), height="400px")
with c2:
    st_pyecharts(charts_lib.airspace_bar(data["airspace"]), height="400px") # Vertical integration

st.markdown("---")
st.markdown("© 2024 Low Altitude Economy Research Institute")

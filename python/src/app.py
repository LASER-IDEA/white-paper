import streamlit as st
from streamlit_echarts import st_pyecharts, st_echarts
import data_factory
import charts
import pandas as pd
import data_processor
import json
import llm_helper
import os

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

st.set_page_config(page_title="Low Altitude Economy Index", layout="wide")

st.title("Low Altitude Economy Development Index")
st.markdown("### White Paper 2024 Dashboard")

# Initialize session state for data
if 'data' not in st.session_state:
    st.session_state.data = data_factory.generate_data()
if 'ts_data' not in st.session_state:
    st.session_state.ts_data = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for CSV Upload
with st.sidebar:
    st.header("Data Upload")

    # Download Sample Button
    data_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_flight_data.csv")
    with open(data_file_path, "rb") as f:
        st.download_button(
            label="Download Sample CSV",
            data=f,
            file_name="sample_flight_data.csv",
            mime="text/csv"
        )

    uploaded_file = st.file_uploader("Upload Flight Data (CSV or JSON)", type=['csv', 'json'])

    if uploaded_file is not None:
        file_type = uploaded_file.name.split('.')[-1].lower()

        if file_type == 'csv':
            if st.button("Compute"):
                try:
                    df = pd.read_csv(uploaded_file)
                    processed_data, ts_data = data_processor.process_csv(df)
                    st.session_state.data = processed_data
                    st.session_state.ts_data = ts_data
                    st.success("Data computed successfully!")
                except Exception as e:
                    st.error(f"Error processing CSV: {e}")

        elif file_type == 'json':
            if st.button("View Dashboard"):
                try:
                    ts_data = json.load(uploaded_file)
                    reconstructed_data = data_processor.reconstruct_streamlit_data(ts_data)
                    st.session_state.data = reconstructed_data
                    st.session_state.ts_data = ts_data
                    st.success("Dashboard view loaded successfully!")
                except Exception as e:
                    st.error(f"Error loading JSON: {e}")


    if st.session_state.ts_data:
        st.divider()
        st.header("Export")
        ts_json = json.dumps(st.session_state.ts_data, indent=2, ensure_ascii=False)
        st.download_button(
            label="Export JSON for White Paper",
            data=ts_json,
            file_name="white_paper_data.json",
            mime="application/json"
        )
        st.info("Exported JSON can be used in the TypeScript visualization application.")

    st.divider()
    st.header("AI Settings")

    # API Key input - never show default value for security
    api_key_placeholder = "Enter your DeepSeek API key" if not os.environ.get("DEEPSEEK_API_KEY") else "API key loaded from .env file"
    api_key = st.text_input("OpenAI/DeepSeek API Key", type="password",
                           placeholder=api_key_placeholder)

    # Show status of API key loading
    if os.environ.get("DEEPSEEK_API_KEY"):
        st.success("✅ API key loaded from .env file")
    else:
        st.warning("⚠️ Please enter your API key or set it in .env file")

    base_url = st.text_input("Base URL (optional, e.g. for DeepSeek)",
                            value=os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"))
    model = st.text_input("Model (leave empty for auto-selection)",
                         value=os.environ.get("DEEPSEEK_CHAT_MODEL", ""),
                         placeholder="Auto-selected based on task complexity")
    st.caption("💡 Auto-selection: 'deepseek-chat' for simple tasks, 'deepseek-reasoner' for complex analysis")

    # Security notice
    with st.expander("🔒 Security Notice"):
        st.markdown("""
        **API Key Security:**
        - Your API key is stored securely in the `.env` file (not committed to version control)
        - The input field above masks your key when typing
        - If no key is entered, the system will use the one from `.env`
        - Never share your API key or commit it to version control
        """)


# Use data from session state
data = st.session_state.data

# Create Tabs
tab1, tab2 = st.tabs(["Dashboard", "AI Assistant"])

with tab1:
    # ----------------- Dashboard Overview -----------------
    st.divider()
    col1, col2 = st.columns([1, 3])
    with col1:
        if "dashboard" in data:
            st_pyecharts(charts.dashboard_chart(data["dashboard"]), height="300px")
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
        if "traffic" in data:
            st_pyecharts(charts.traffic_area_chart(data["traffic"]), height="400px")
    with col2:
        if "operation" in data:
            st_pyecharts(charts.operation_dual_line(data["operation"]), height="400px")

    # ----------------- 2. Structure & Entity -----------------
    st.header("2. Structure & Entity")
    c1, c2, c3 = st.columns(3)
    with c1:
        if "fleet" in data:
            st_pyecharts(charts.fleet_stacked_bar(data["fleet"]), height="350px")
    with c2:
        if "pareto" in data:
            st_pyecharts(charts.pareto_chart(data["pareto"]), height="350px")
    with c3:
        if "rose" in data:
            st_pyecharts(charts.rose_chart(data["rose"]), height="350px")

    if "treemap" in data:
        st_pyecharts(charts.treemap_chart(data["treemap"]), height="400px")

    # ----------------- 3. Time & Space -----------------
    st.header("3. Time & Space")
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("Regional Heatmap")
        if "map" in data:
            map_result = charts.map_chart(data["map"])
            st_echarts(map_result["options"], map=map_result["map"], height="500px")
    with c2:
        if "polar" in data:
            st_pyecharts(charts.polar_clock_chart(data["polar"]), height="500px")

    st.subheader("Calendar Activity")
    if "calendar" in data:
        st_pyecharts(charts.calendar_heatmap(data["calendar"]), height="250px")

    c1, c2 = st.columns(2)
    with c1:
        if "night" in data:
            st_pyecharts(charts.night_wave_chart(data["night"]), height="300px")
    with c2:
        if "chord" in data:
            st_pyecharts(charts.chord_chart(data["chord"]), height="400px")

    # ----------------- 4. Efficiency & Quality -----------------
    st.header("4. Efficiency & Quality")
    c1, c2, c3 = st.columns(3)
    with c1:
        if "seasonal" in data:
            st_pyecharts(charts.seasonal_boxplot(data["seasonal"]), height="350px")
    with c2:
        if "gauge" in data:
            st_pyecharts(charts.gauge_chart(data["gauge"]), height="350px")
    with c3:
        if "funnel" in data:
            st_pyecharts(charts.funnel_chart(data["funnel"]), height="350px")

    if "histogram" in data:
        st_pyecharts(charts.histogram_chart(data["histogram"]), height="300px")

    # ----------------- 5. Innovation & Integration -----------------
    st.header("5. Innovation & Integration")
    c1, c2 = st.columns(2)
    with c1:
        if "radar" in data:
            st_pyecharts(charts.radar_chart(data["radar"]), height="400px")
    with c2:
        if "airspace" in data:
            st_pyecharts(charts.airspace_bar(data["airspace"]), height="400px")

    st.markdown("---")
    st.markdown("© 2024 Low Altitude Economy Research Institute")


with tab2:
    st.header("AI Data Analyst")
    st.markdown("Ask questions about the Low Altitude Economy data, and the AI will infer indices and visualize them.")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "chart_code" in message and message["chart_code"]:
                try:
                    # Execute the chart code to get the chart object
                    local_scope = {}
                    exec(message["chart_code"], globals(), local_scope)
                    if "chart" in local_scope:
                        st_pyecharts(local_scope["chart"], height="400px")
                except Exception as e:
                    st.error(f"Error rendering chart: {e}")

    # Chat input
    if prompt := st.chat_input("What would you like to visualize? (e.g. 'Compare the growth rate of different aircraft types')"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking and visualizing..."):
                explanation, code = llm_helper.get_llm_response(
                    prompt,
                    st.session_state.data,
                    api_key=api_key,
                    base_url=base_url if base_url else None,
                    model=model
                )

                st.markdown(explanation)

                if code:
                    try:
                        local_scope = {}
                        exec(code, globals(), local_scope)
                        if "chart" in local_scope:
                            st_pyecharts(local_scope["chart"], height="400px")
                        else:
                            st.warning("The AI generated code but didn't assign the chart to a variable named 'chart'.")
                    except Exception as e:
                        st.error(f"Failed to render visualization. Error: {e}")
                        st.code(code, language="python")

        # Add assistant response to chat history
        st.session_state.messages.append({
            "role": "assistant",
            "content": explanation,
            "chart_code": code
        })

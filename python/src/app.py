import streamlit as st
from streamlit_echarts import st_pyecharts, st_echarts
import data_factory
import charts
import pandas as pd
import data_processor
import json
import llm_helper
import os
import re
import ast
from pathlib import Path

# Import knowledge base module
try:
    import knowledge_base
    KNOWLEDGE_BASE_AVAILABLE = True
except ImportError:
    KNOWLEDGE_BASE_AVAILABLE = False

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Constants for validation
MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
MAX_CSV_ROWS = 100000
MAX_CODE_LINES = 100

def validate_and_execute_chart_code(code: str, max_lines: int = MAX_CODE_LINES) -> tuple:
    """
    Safely validate and execute chart generation code.
    
    Args:
        code: The Python code to validate and execute
        max_lines: Maximum number of lines allowed (default: MAX_CODE_LINES)
        
    Returns:
        tuple: (success: bool, result_or_error: any)
    """
    if not code or not isinstance(code, str):
        return False, "Invalid code provided"
    
    # Check code length
    lines = code.strip().split('\n')
    if len(lines) > max_lines:
        return False, f"Code exceeds maximum allowed lines ({max_lines})"
    
    # Validate code structure using AST
    try:
        parsed = ast.parse(code)
    except SyntaxError as e:
        return False, f"Syntax error in generated code: {e}"
    
    # Check for dangerous operations
    # Note: We're being strict here - dunder methods in string context are blocked
    # But legitimate uses like class.__name__ in imports are allowed via AST validation
    dangerous_patterns = [
        r'\b(eval|compile|__import__|open|file)\s*\(',
        r'\bos\.(system|popen|spawn|exec)',
        r'\bsubprocess\.',
        r'__\w+__\s*\(',  # Only block dunder method calls, not attributes
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, code):
            return False, f"Code contains potentially unsafe operations"
    
    # Allow only specific safe imports
    allowed_imports = {
        'pyecharts', 'pyecharts.charts', 'pyecharts.options',
        'pandas', 'numpy', 'datetime', 'math'
    }
    
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            if isinstance(node, ast.ImportFrom):
                module = node.module
                if module and not any(module.startswith(allowed) for allowed in allowed_imports):
                    return False, f"Import not allowed: {module}"
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if not any(alias.name.startswith(allowed) for allowed in allowed_imports):
                        return False, f"Import not allowed: {alias.name}"
    
    # Execute in a restricted scope
    try:
        local_scope = {}
        # Only provide access to safe modules
        safe_globals = {
            '__builtins__': {
                'range': range,
                'len': len,
                'str': str,
                'int': int,
                'float': float,
                'list': list,
                'dict': dict,
                'tuple': tuple,
                'set': set,
                'True': True,
                'False': False,
                'None': None,
            }
        }
        exec(code, safe_globals, local_scope)
        
        if "chart" in local_scope:
            return True, local_scope["chart"]
        else:
            return False, "Code executed but didn't create a 'chart' variable"
            
    except Exception as e:
        return False, f"Execution error: {str(e)}"

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

# Initialize knowledge base if available
if 'kb' not in st.session_state:
    if KNOWLEDGE_BASE_AVAILABLE:
        with st.spinner("Initializing knowledge base..."):
            st.session_state.kb = knowledge_base.initialize_knowledge_base()
            if st.session_state.kb:
                st.success("✅ Knowledge base initialized with white paper documents")
    else:
        st.session_state.kb = None

# Sidebar for CSV Upload
with st.sidebar:
    st.header("Data Upload")

    # Download Sample Button with safer path handling
    try:
        base_path = Path(__file__).parent.parent
        data_file_path = (base_path / "data" / "sample_flight_data.csv").resolve()
        
        # Ensure the path is within the expected directory
        if not data_file_path.is_relative_to(base_path):
            st.error("Invalid file path")
        elif data_file_path.exists():
            with open(data_file_path, "rb") as f:
                st.download_button(
                    label="Download Sample CSV",
                    data=f,
                    file_name="sample_flight_data.csv",
                    mime="text/csv"
                )
        else:
            st.warning("Sample data file not found")
    except Exception as e:
        st.error(f"Error loading sample file: {e}")

    uploaded_file = st.file_uploader("Upload Flight Data (CSV or JSON)", type=['csv', 'json'])

    if uploaded_file is not None:
        # Validate file size
        file_size = uploaded_file.size
        
        if file_size > MAX_FILE_SIZE_BYTES:
            st.error(f"File size ({file_size / (1024*1024):.2f} MB) exceeds maximum allowed size ({MAX_FILE_SIZE_MB} MB)")
        else:
            file_type = uploaded_file.name.split('.')[-1].lower()

            if file_type == 'csv':
                if st.button("Compute"):
                    try:
                        # Read CSV with size limit and error handling
                        df = pd.read_csv(uploaded_file, nrows=MAX_CSV_ROWS)
                        
                        if df.empty:
                            st.error("CSV file is empty")
                        else:
                            processed_data, ts_data = data_processor.process_csv(df)
                            st.session_state.data = processed_data
                            st.session_state.ts_data = ts_data
                            st.success("Data computed successfully!")
                    except pd.errors.ParserError as e:
                        st.error(f"Invalid CSV format: {e}")
                    except pd.errors.EmptyDataError:
                        st.error("CSV file contains no data")
                    except Exception as e:
                        st.error(f"Error processing CSV: {e}")

            elif file_type == 'json':
                if st.button("View Dashboard"):
                    try:
                        ts_data = json.load(uploaded_file)
                        
                        # Basic validation of JSON structure
                        if not isinstance(ts_data, dict):
                            st.error("Invalid JSON format: expected a JSON object")
                        else:
                            reconstructed_data = data_processor.reconstruct_streamlit_data(ts_data)
                            st.session_state.data = reconstructed_data
                            st.session_state.ts_data = ts_data
                            st.success("Dashboard view loaded successfully!")
                    except json.JSONDecodeError as e:
                        st.error(f"Invalid JSON format: {e}")
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
    col1, col2, col3 = st.columns(3)
    with col1:
        if "traffic" in data:
            st_pyecharts(charts.traffic_area_chart(data["traffic"]), height="350px")
    with col2:
        if "operation" in data:
            st_pyecharts(charts.operation_dual_line(data["operation"]), height="350px")
    with col3:
        if "growth" in data:
            st_pyecharts(charts.growth_area_chart(data["growth"]), height="350px")

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

    if "hub" in data:
        st_pyecharts(charts.hub_graph_chart(data["hub"]), height="500px")

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

    # Full width for control chart
    if "quality" in data:
        st.subheader("任务完成质量控制图")
        quality_options = charts.quality_control_chart(data["quality"])
        if quality_options:
            st_echarts(quality_options, height="600px")

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
    
    # Display knowledge base status
    if st.session_state.kb:
        st.info("🧠 RAG Knowledge Base Active: AI responses are enhanced with information from white paper documents")
    else:
        if KNOWLEDGE_BASE_AVAILABLE:
            st.warning("⚠️ Knowledge base initialization failed. AI will work without RAG context.")
        else:
            st.info("💡 Install RAG dependencies for enhanced AI responses: `pip install langchain langchain-community chromadb pypdf sentence-transformers`")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "chart_code" in message and message["chart_code"]:
                # Safely execute the chart code
                success, result = validate_and_execute_chart_code(message["chart_code"])
                if success:
                    st_pyecharts(result, height="400px")
                else:
                    st.error(f"Error rendering chart: {result}")

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
                    model=model,
                    knowledge_base=st.session_state.kb
                )

                st.markdown(explanation)

                if code:
                    # Safely execute the generated code
                    success, result = validate_and_execute_chart_code(code)
                    if success:
                        st_pyecharts(result, height="400px")
                    else:
                        st.error(f"Failed to render visualization: {result}")
                        st.code(code, language="python")

        # Add assistant response to chat history
        st.session_state.messages.append({
            "role": "assistant",
            "content": explanation,
            "chart_code": code
        })

"""
LAEV-Agents Professional Demo
A Streamlit-based web interface for the Low Altitude Economy Visualization system.
"""

import streamlit as st
import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# Add parent path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "python" / "src"))

# Page configuration must be first
st.set_page_config(
    page_title="LAEV-Agents | Intelligent Visualization",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Main container */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Header styling */
    .stApp header {
        background: linear-gradient(90deg, #002FA7 0%, #1E5AA8 100%);
    }
    
    /* Title styling */
    h1 {
        color: #002FA7 !important;
        font-weight: 700 !important;
    }
    
    h2, h3 {
        color: #1a365d !important;
    }
    
    /* Card styling */
    .stCard {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
    }
    
    /* Query input styling */
    .stTextArea textarea {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        font-size: 16px;
        padding: 12px;
    }
    
    .stTextArea textarea:focus {
        border-color: #002FA7;
        box-shadow: 0 0 0 3px rgba(0, 47, 167, 0.1);
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #002FA7 0%, #1E5AA8 100%) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 12px 32px !important;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: 0 4px 6px rgba(0, 47, 167, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(0, 47, 167, 0.4) !important;
    }
    
    /* Status badges */
    .status-success {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    
    .status-error {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    
    .status-processing {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    
    /* Agent timeline */
    .agent-card {
        background: white;
        border-left: 4px solid #002FA7;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 8px 8px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .agent-name {
        font-weight: 700;
        color: #002FA7;
        font-size: 14px;
    }
    
    .agent-action {
        color: #4a5568;
        font-size: 13px;
        margin-top: 5px;
    }
    
    /* Metrics cards */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #002FA7;
    }
    
    .metric-label {
        font-size: 14px;
        color: #718096;
        margin-top: 5px;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a365d 0%, #2d4a6f 100%);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #f7fafc;
        border-radius: 8px;
        font-weight: 600;
    }
    
    /* Code block */
    .stCodeBlock {
        border-radius: 8px;
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
        border-left: 4px solid #0ea5e9;
        padding: 16px;
        border-radius: 0 8px 8px 0;
        margin: 10px 0;
    }
    
    /* Example queries */
    .example-query {
        background: #f7fafc;
        border: 1px solid #e2e8f0;
        padding: 10px 15px;
        border-radius: 8px;
        margin: 5px 0;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .example-query:hover {
        background: #edf2f7;
        border-color: #002FA7;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = None
if 'current_result' not in st.session_state:
    st.session_state.current_result = None

# Example queries
EXAMPLE_QUERIES = [
    "Show the trend of flight operations over time",
    "Compare flight duration across different regions",
    "Display the distribution of aircraft types",
    "What is the relationship between weather and flight delays?",
    "Provide a comprehensive dashboard of low-altitude economy operations",
    "Identify any unusual flight patterns or anomalies"
]

def init_orchestrator(use_full: bool = False, max_iterations: int = 3):
    """Initialize the orchestrator with selected settings."""
    try:
        from agents import LAEVOrchestrator
        
        llm_provider = st.session_state.get('llm_provider', 'deepseek')
        
        with st.spinner("🚀 Initializing LAEV-Agents system..."):
            orchestrator = LAEVOrchestrator(
                llm_provider=llm_provider,
                use_full_agents=use_full,
                max_iterations=max_iterations
            )
        return orchestrator
    except Exception as e:
        st.error(f"Failed to initialize system: {str(e)}")
        return None

def process_query(query: str) -> Dict[str, Any]:
    """Process user query through the system."""
    if not st.session_state.orchestrator:
        st.session_state.orchestrator = init_orchestrator(
            use_full=st.session_state.get('use_full_agents', False),
            max_iterations=st.session_state.get('max_iterations', 3)
        )
    
    if st.session_state.orchestrator:
        start_time = time.time()
        result = st.session_state.orchestrator.process(query)
        result['processing_time'] = time.time() - start_time
        return result
    
    return {"success": False, "error": "System not initialized"}

def render_header():
    """Render application header."""
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h1 style="font-size: 42px; margin-bottom: 10px;">
                ✈️ LAEV-Agents
            </h1>
            <p style="font-size: 18px; color: #4a5568; margin-top: 0;">
                Intelligent Visualization for Low Altitude Economy
            </p>
            <p style="font-size: 14px; color: #718096;">
                Multi-Agent System with GraphRAG • IEEE VIS 2026
            </p>
        </div>
        """, unsafe_allow_html=True)

def render_sidebar():
    """Render sidebar with settings and information."""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 10px 0;">
            <h2 style="color: white; font-size: 24px;">⚙️ Settings</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # LLM Provider selection
        st.session_state.llm_provider = st.selectbox(
            "🤖 LLM Provider",
            options=["deepseek", "openai", "anthropic"],
            index=0,
            help="Select the language model provider"
        )
        
        # Agent mode
        st.session_state.use_full_agents = st.toggle(
            "🔧 Full Agent Mode",
            value=False,
            help="Enable full agent implementation with visual evaluation"
        )
        
        # Max iterations
        st.session_state.max_iterations = st.slider(
            "🔄 Max Iterations",
            min_value=1,
            max_value=5,
            value=3,
            help="Maximum refinement iterations"
        )
        
        st.divider()
        
        # System info
        st.markdown("""
        <div style="color: #a0aec0; font-size: 12px;">
            <p><strong>System Components:</strong></p>
            <ul>
                <li>Planner Agent</li>
                <li>Retriever Agent (GraphRAG)</li>
                <li>Coder Agent</li>
                <li>Evaluator Agent</li>
                <li>Reflector Agent</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Initialize button
        if st.button("🚀 Initialize System", use_container_width=True):
            st.session_state.orchestrator = init_orchestrator(
                use_full=st.session_state.use_full_agents,
                max_iterations=st.session_state.max_iterations
            )
            if st.session_state.orchestrator:
                st.success("✅ System ready!")

def render_query_section():
    """Render query input section."""
    st.markdown("### 📝 Enter Your Query")
    
    # Query input
    query = st.text_area(
        "",
        placeholder="Describe the visualization you want to create...",
        height=100,
        key="query_input",
        label_visibility="collapsed"
    )
    
    # Example queries
    st.markdown("<p style='color: #718096; font-size: 14px; margin-top: 10px;'>💡 Example queries:</p>", 
                unsafe_allow_html=True)
    
    cols = st.columns(3)
    for i, example in enumerate(EXAMPLE_QUERIES[:3]):
        with cols[i]:
            if st.button(f"📊 {example[:25]}...", key=f"ex_{i}"):
                st.session_state.query_input = example
                st.rerun()
    
    cols = st.columns(3)
    for i, example in enumerate(EXAMPLE_QUERIES[3:6]):
        with cols[i]:
            if st.button(f"📈 {example[:25]}...", key=f"ex_{i+3}"):
                st.session_state.query_input = example
                st.rerun()
    
    # Generate button
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        generate_clicked = st.button(
            "✨ Generate Visualization",
            use_container_width=True,
            type="primary"
        )
    
    return query, generate_clicked

def render_agent_timeline(result: Dict[str, Any]):
    """Render agent execution timeline."""
    st.markdown("### 🔄 Agent Execution Timeline")
    
    agent_trace = result.get('agent_trace', [])
    iterations = result.get('iterations', 1)
    
    # Timeline container
    with st.container():
        # Show iterations
        st.info(f"📊 Completed in **{iterations}** iteration(s)")
        
        # Group by agent
        agent_colors = {
            'PlannerAgent': '#002FA7',
            'RetrieverAgent': '#059669',
            'CoderAgent': '#d97706',
            'EvaluatorAgent': '#7c3aed',
            'ReflectorAgent': '#dc2626'
        }
        
        for i, log in enumerate(agent_trace[-10:]):  # Show last 10 logs
            agent_name = log.get('agent', 'Unknown')
            action = log.get('action', 'Processing')
            details = log.get('details', {})
            
            color = agent_colors.get(agent_name, '#718096')
            
            st.markdown(f"""
            <div class="agent-card" style="border-left-color: {color};">
                <div class="agent-name">{agent_name}</div>
                <div class="agent-action">{action}</div>
            </div>
            """, unsafe_allow_html=True)

def render_result(result: Dict[str, Any]):
    """Render visualization result."""
    st.markdown("---")
    st.markdown("## 📊 Visualization Result")
    
    # Status
    success = result.get('success', False)
    
    if success:
        st.success("✅ Visualization generated successfully!")
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("⏱️ Processing Time", f"{result.get('processing_time', 0):.1f}s")
        with col2:
            st.metric("🔄 Iterations", result.get('iterations', 1))
        with col3:
            quality_score = result.get('visual_feedback', {}).get('overall_score', 'N/A')
            if isinstance(quality_score, (int, float)):
                quality_score = f"{quality_score:.2f}"
            st.metric("⭐ Quality Score", quality_score)
        with col4:
            st.metric("📈 Status", "Success" if success else "Failed")
        
        # Chart display
        chart_html = result.get('chart_html')
        if chart_html:
            st.markdown("### 📈 Generated Chart")
            st.components.v1.html(chart_html, height=500, scrolling=True)
        
        # Agent timeline
        with st.expander("🔍 View Agent Execution Details"):
            render_agent_timeline(result)
        
        # Code view
        with st.expander("💻 View Generated Code"):
            chart_code = result.get('chart_code', '')
            st.code(chart_code, language='python')
        
    else:
        st.error("❌ Failed to generate visualization")
        error_msg = result.get('error', 'Unknown error')
        st.error(f"Error: {error_msg}")
        
        # Show trace for debugging
        with st.expander("🔍 Debug Information"):
            render_agent_timeline(result)

def render_history():
    """Render query history."""
    if st.session_state.history:
        st.markdown("---")
        st.markdown("## 🕐 Recent Queries")
        
        for i, item in enumerate(reversed(st.session_state.history[-5:])):
            with st.container():
                cols = st.columns([4, 1, 1])
                with cols[0]:
                    st.markdown(f"**{item['query'][:60]}...**" if len(item['query']) > 60 
                               else f"**{item['query']}**")
                with cols[1]:
                    status_color = "🟢" if item['success'] else "🔴"
                    st.markdown(f"{status_color} {item['time']}")
                with cols[2]:
                    if st.button("🔄 Rerun", key=f"rerun_{i}"):
                        st.session_state.query_input = item['query']
                        st.rerun()

def main():
    """Main application."""
    render_header()
    render_sidebar()
    
    # Main content
    query, generate_clicked = render_query_section()
    
    # Process query
    if generate_clicked and query:
        with st.spinner("🤖 Processing your query..."):
            result = process_query(query)
            st.session_state.current_result = result
            
            # Add to history
            st.session_state.history.append({
                'query': query,
                'success': result.get('success', False),
                'time': datetime.now().strftime("%H:%M:%S")
            })
    
    # Display result
    if st.session_state.current_result:
        render_result(st.session_state.current_result)
    
    # Display history
    render_history()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #718096; padding: 20px;">
        <p>LAEV-Agents Demo | IEEE VIS 2026 Submission</p>
        <p style="font-size: 12px;">Powered by DeepSeek-V2, PyECharts, and GraphRAG</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

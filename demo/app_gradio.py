"""
LAEV-Agents Gradio Demo
Alternative interface using Gradio for broader compatibility.
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, Any, Tuple

# Add parent path
sys.path.insert(0, str(Path(__file__).parent.parent / "python" / "src"))

import gradio as gr
import pandas as pd

# Global orchestrator instance
_orchestrator = None

def get_orchestrator(use_full: bool = False, max_iter: int = 3, provider: str = "deepseek"):
    """Get or create orchestrator instance."""
    global _orchestrator
    if _orchestrator is None:
        from agents import LAEVOrchestrator
        _orchestrator = LAEVOrchestrator(
            llm_provider=provider,
            use_full_agents=use_full,
            max_iterations=max_iter
        )
    return _orchestrator

def process_query(
    query: str,
    provider: str,
    use_full: bool,
    max_iter: int
) -> Tuple[str, str, str]:
    """Process query and return results."""
    if not query.strip():
        return "Please enter a query", "", ""
    
    try:
        orchestrator = get_orchestrator(use_full, max_iter, provider)
        
        start_time = time.time()
        result = orchestrator.process(query)
        processing_time = time.time() - start_time
        
        # Format status
        success = result.get('success', False)
        status = "✅ Success" if success else "❌ Failed"
        
        # Format metrics
        metrics = f"""
**Processing Time:** {processing_time:.2f}s
**Iterations:** {result.get('iterations', 1)}
**Quality Score:** {result.get('visual_feedback', {}).get('overall_score', 'N/A')}
**Status:** {status}
        """.strip()
        
        # Format agent trace
        trace_lines = []
        for log in result.get('agent_trace', [])[-8:]:
            agent = log.get('agent', 'Unknown')
            action = log.get('action', '')
            trace_lines.append(f"**{agent}**: {action}")
        agent_trace = "\n\n".join(trace_lines)
        
        # Chart HTML
        chart_html = result.get('chart_html', '<p>No chart generated</p>')
        
        return metrics, agent_trace, chart_html
        
    except Exception as e:
        return f"Error: {str(e)}", "", ""

def create_demo():
    """Create Gradio interface."""
    
    # Custom CSS
    css = """
    .gradio-container {
        font-family: 'Inter', sans-serif;
    }
    .header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .header h1 {
        color: #002FA7;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .header p {
        color: #4a5568;
        font-size: 1.1rem;
    }
    """
    
    with gr.Blocks(css=css, title="LAEV-Agents Demo") as demo:
        
        # Header
        gr.HTML("""
        <div class="header">
            <h1>✈️ LAEV-Agents</h1>
            <p>Intelligent Visualization for Low Altitude Economy</p>
            <p style="font-size: 0.9rem; color: #718096;">Multi-Agent System with GraphRAG • IEEE VIS 2026</p>
        </div>
        """)
        
        with gr.Row():
            # Left panel - Settings and Input
            with gr.Column(scale=1):
                gr.Markdown("### ⚙️ Settings")
                
                provider = gr.Dropdown(
                    choices=["deepseek", "openai", "anthropic"],
                    value="deepseek",
                    label="🤖 LLM Provider"
                )
                
                use_full = gr.Checkbox(
                    label="🔧 Full Agent Mode",
                    value=False,
                    info="Enable visual evaluation"
                )
                
                max_iter = gr.Slider(
                    minimum=1,
                    maximum=5,
                    value=3,
                    step=1,
                    label="🔄 Max Iterations"
                )
                
                gr.Markdown("---")
                gr.Markdown("### 📝 Query")
                
                query_input = gr.Textbox(
                    label="",
                    placeholder="Describe the visualization you want...",
                    lines=3
                )
                
                # Example buttons
                gr.Markdown("**💡 Examples:**")
                with gr.Row():
                    ex1 = gr.Button("Trend Analysis", size="sm")
                    ex2 = gr.Button("Comparison", size="sm")
                with gr.Row():
                    ex3 = gr.Button("Distribution", size="sm")
                    ex4 = gr.Button("Dashboard", size="sm")
                
                submit_btn = gr.Button(
                    "✨ Generate Visualization",
                    variant="primary",
                    size="lg"
                )
                
                gr.Markdown("---")
                gr.Markdown("#### 📊 Metrics")
                metrics_output = gr.Markdown()
            
            # Right panel - Results
            with gr.Column(scale=2):
                gr.Markdown("### 📈 Visualization")
                chart_output = gr.HTML()
                
                with gr.Accordion("🔍 Agent Execution Trace", open=False):
                    trace_output = gr.Markdown()
        
        # Event handlers
        def set_example(text):
            return text
        
        ex1.click(lambda: set_example("Show the trend of flight operations over time"), outputs=query_input)
        ex2.click(lambda: set_example("Compare flight duration across different regions"), outputs=query_input)
        ex3.click(lambda: set_example("Display the distribution of aircraft types"), outputs=query_input)
        ex4.click(lambda: set_example("Provide a comprehensive dashboard of operations"), outputs=query_input)
        
        submit_btn.click(
            fn=process_query,
            inputs=[query_input, provider, use_full, max_iter],
            outputs=[metrics_output, trace_output, chart_output]
        )
        
        # Footer
        gr.Markdown("---")
        gr.Markdown(
            "<div style='text-align: center; color: #718096;'>"
            "LAEV-Agents Demo | IEEE VIS 2026 | Powered by DeepSeek-V2, PyECharts, and GraphRAG"
            "</div>"
        )
    
    return demo

if __name__ == "__main__":
    demo = create_demo()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )

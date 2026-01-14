import os
import json
import re
import streamlit as st
import pandas as pd

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, will use environment variables directly

# Handle optional openai dependency
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

def summarize_data(data):
    """
    Creates a summary of the data structure (keys, types, sample values)
    to be efficient for the LLM prompt.
    """
    summary = []

    if isinstance(data, dict):
        summary.append("Data is a dictionary with the following keys:")
        for key, value in data.items():
            if isinstance(value, list):
                if len(value) > 0:
                    sample = value[0]
                    summary.append(f"- '{key}': List of {len(value)} items. Sample item: {str(sample)[:200]}...")
                else:
                    summary.append(f"- '{key}': Empty list")
            elif isinstance(value, dict):
                 summary.append(f"- '{key}': Dictionary with keys: {list(value.keys())}")
            elif isinstance(value, pd.DataFrame):
                summary.append(f"- '{key}': DataFrame with columns: {list(value.columns)}. Sample:\n{value.head(2).to_string()}")
            else:
                summary.append(f"- '{key}': {type(value).__name__} ({str(value)[:100]})")

    elif isinstance(data, pd.DataFrame):
        summary.append("Data is a pandas DataFrame:")
        summary.append(f"Columns: {list(data.columns)}")
        summary.append(f"Shape: {data.shape}")
        summary.append("Sample rows:")
        summary.append(data.head(3).to_string())

    else:
        summary.append(f"Data type: {type(data).__name__}")
        summary.append(f"String representation (truncated): {str(data)[:500]}...")

    return "\n".join(summary)

def determine_task_complexity(query):
    """
    Determine if a task requires complex reasoning or is simple.
    Returns True for complex tasks (use deepseek-reasoner), False for simple tasks (use deepseek-chat).
    """
    query_lower = query.lower()

    # Keywords that indicate complex reasoning tasks
    complex_keywords = [
        'analyze', 'compare', 'correlation', 'trend', 'pattern', 'relationship',
        'calculate', 'compute', 'optimize', 'forecast', 'predict', 'model',
        'evaluate', 'assess', 'interpret', 'explain', 'why', 'how',
        'inference', 'conclusion', 'recommend', 'strategy', 'impact',
        'efficiency', 'performance', 'optimization', 'benchmark'
    ]

    # Check for complex keywords
    for keyword in complex_keywords:
        if keyword in query_lower:
            return True

    # Check query length (longer queries tend to be more complex)
    if len(query.split()) > 20:
        return True

    # Check for multiple questions or complex structure
    if query.count('?') > 1 or ' and ' in query_lower or ' or ' in query_lower:
        return True

    return False

def get_llm_response(query, data_context, api_key=None, base_url=None, model=None):
    """
    Interact with the LLM to generate a visualization based on the query and data context.

    Args:
        query (str): The user's question or request.
        data_context (dict or pd.DataFrame): The available data to work with.
        api_key (str, optional): OpenAI compatible API key. If None, uses DEEPSEEK_API_KEY from .env.
        base_url (str, optional): OpenAI compatible base URL. If None, uses DEEPSEEK_BASE_URL from .env.
        model (str, optional): Model name to use. If None, auto-selects based on task complexity.

    Returns:
        tuple: (explanation, code)
        explanation (str): The text response from the LLM.
        code (str): The generated Python code to create the chart.
    """

    # Load configuration from .env if not provided
    if not api_key:
        api_key = os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("OPENAI_API_KEY")

    if not base_url:
        base_url = os.environ.get("DEEPSEEK_BASE_URL")

    # Auto-select model based on task complexity if not specified
    if not model:
        is_complex = determine_task_complexity(query)
        if is_complex:
            model = os.environ.get("DEEPSEEK_REASONER_MODEL", "deepseek-reasoner")
        else:
            model = os.environ.get("DEEPSEEK_CHAT_MODEL", "deepseek-chat")

    if not api_key:
        # Fallback for testing without key - returns a mock bar chart
        explanation = "I need an API key to process your request using a real LLM. However, I can demonstrate how this would work with a mock example. Here is a sample chart generated based on a hypothetical interpretation of your request."

        code = """
from pyecharts.charts import Bar
from pyecharts import options as opts

# Mock data generation based on the idea of 'inferring new indices'
# Assuming we want to show some calculated index
categories = ["Index A", "Index B", "Index C", "Index D", "Index E"]
values = [85, 72, 90, 65, 88]

c = (
    Bar()
    .add_xaxis(categories)
    .add_yaxis("Calculated Index", values, color="#3b82f6")
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Inferred Index Visualization (Mock)"),
        yaxis_opts=opts.AxisOpts(name="Value"),
        xaxis_opts=opts.AxisOpts(name="Category")
    )
)
chart = c
"""
        return explanation, code

    if OpenAI is None:
        return "The 'openai' library is not installed. Please install it to use this feature.", None

    client = OpenAI(api_key=api_key, base_url=base_url)

    # Construct the system prompt
    # We describe the environment and available libraries (pyecharts)
    system_prompt = """
You are a data analysis assistant for a Low Altitude Economy dashboard.
Your goal is to help the user understand the data and visualize new indices or insights.
You have access to the data in the variable `data`.
The `data` is a dictionary or dataframe containing metrics about flights, fleet, etc.

When asked to visualize something:
1. Infer the necessary calculation or data transformation.
2. Generate Python code using `pyecharts` to create the visualization.
3. The code MUST assign the final chart object to a variable named `chart`.
4. Do NOT use `chart.render()`, just assign the object.
5. Use the `pyecharts.options` as `opts`.
6. Explain your reasoning briefly before or after the code block.

Available data context structure:
{data_summary}

Example Output Format:
Here is the analysis of the data...

```python
from pyecharts.charts import Bar
from pyecharts import options as opts

c = (
    Bar()
    .add_xaxis(...)
    .add_yaxis(...)
    .set_global_opts(...)
)
chart = c
```
"""

    # Create a summary of the data structure to send to the LLM
    data_summary = summarize_data(data_context)

    formatted_system_prompt = system_prompt.replace("{data_summary}", data_summary)

    messages = [
        {"role": "system", "content": formatted_system_prompt},
        {"role": "user", "content": query}
    ]

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        content = response.choices[0].message.content

        # Extract code block
        code_match = re.search(r"```python(.*?)```", content, re.DOTALL)
        if code_match:
            code = code_match.group(1).strip()
            explanation = content
        else:
            code = None
            explanation = content

        return explanation, code

    except Exception as e:
        return f"Error communicating with LLM: {str(e)}", None

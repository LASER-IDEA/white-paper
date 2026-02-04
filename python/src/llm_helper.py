import os
import json
import re
import streamlit as st
import pandas as pd
from typing import Tuple, Optional, Union, Dict, List

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

# Import KnowledgeBase
try:
    from knowledge_base import KnowledgeBase
except ImportError:
    try:
        from .knowledge_base import KnowledgeBase
    except ImportError:
        KnowledgeBase = None

# Type alias for data that can be summarized
DataType = Union[Dict, pd.DataFrame]

# Global KB instance
_kb = None

def _get_kb():
    global _kb
    if _kb is None and KnowledgeBase:
        try:
            # Try to find the docs directory relative to where we are running
            # Default to docs/latex/sections assuming running from project root
            _kb = KnowledgeBase()
        except Exception as e:
            print(f"Failed to load KnowledgeBase: {e}")
            return None
    return _kb

def summarize_data(data: DataType) -> str:
    """
    Creates a summary of the data structure (keys, types, sample values)
    to be efficient for the LLM prompt.
    """
    summary: List[str] = []

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

def determine_task_complexity(query: str) -> bool:
    """
    Determine if a task requires complex reasoning or is simple.
    """
    query_lower = query.lower()
    complex_keywords = [
        'analyze', 'compare', 'correlation', 'trend', 'pattern', 'relationship',
        'calculate', 'compute', 'optimize', 'forecast', 'predict', 'model',
        'evaluate', 'assess', 'interpret', 'explain', 'why', 'how',
        'inference', 'conclusion', 'recommend', 'strategy', 'impact',
        'efficiency', 'performance', 'optimization', 'benchmark'
    ]

    for keyword in complex_keywords:
        if keyword in query_lower:
            return True

    if len(query.split()) > 20:
        return True

    if query.count('?') > 1 or ' and ' in query_lower or ' or ' in query_lower:
        return True

    return False

def get_api_config(api_key=None, base_url=None, model=None, query=""):
    """Helper to get API config from args or env"""
    if not api_key:
        api_key = os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("OPENAI_API_KEY")

    if not base_url:
        base_url = os.environ.get("DEEPSEEK_BASE_URL")

    if not model:
        is_complex = determine_task_complexity(query) if query else False
        if is_complex:
            model = os.environ.get("DEEPSEEK_REASONER_MODEL", "deepseek-reasoner")
        else:
            model = os.environ.get("DEEPSEEK_CHAT_MODEL", "deepseek-chat")

    return api_key, base_url, model

def get_llm_response(
    query: str, 
    data_context: DataType, 
    api_key: Optional[str] = None, 
    base_url: Optional[str] = None, 
    model: Optional[str] = None
) -> Tuple[str, Optional[str]]:
    """
    Interact with the LLM to generate a visualization based on the query and data context.
    Uses RAG to include knowledge from the Blue Book.
    """
    api_key, base_url, model = get_api_config(api_key, base_url, model, query)

    # RAG Retrieval
    kb = _get_kb()
    kb_context = ""
    if kb:
        # Search for relevant documents
        # We increase top_k to get enough context
        docs = kb.search(query, 5)
        if docs:
            kb_context = "\n\nRelevant Content from 'Low Altitude Economy Blue Book' (Reference):\n"
            for d in docs:
                kb_context += f"--- Section: {d.section} ---\n{d.content}\n"
        else:
             # Fallback: if query is very generic, maybe provide introduction?
             pass

    if not api_key:
        # Fallback for testing without key
        explanation = "I need an API key to process your request using a real LLM. (Mock Response with RAG info if available)"
        if kb_context:
            explanation += f"\n\nI found some relevant info in the Blue Book:\n{kb_context[:500]}..."

        code = """
from pyecharts.charts import Bar
from pyecharts import options as opts

# Mock data generation
categories = ["A", "B", "C", "D", "E"]
values = [10, 20, 30, 40, 50]

c = (
    Bar()
    .add_xaxis(categories)
    .add_yaxis("Mock Series", values)
    .set_global_opts(title_opts=opts.TitleOpts(title="Mock Chart"))
)
chart = c
"""
        return explanation, code

    if OpenAI is None:
        return "The 'openai' library is not installed.", None

    client = OpenAI(api_key=api_key, base_url=base_url)

    # Construct the system prompt
    # We describe the environment and available libraries (pyecharts)
    system_prompt = """
You are a data analysis assistant for a Low Altitude Economy dashboard.
Your goal is to help the user understand the data and visualize new indices or insights.
You have access to the data in the variable `data`.
The `data` is a dictionary or dataframe containing metrics about flights, fleet, etc.

You also have access to the "Low Altitude Economy Blue Book" content below.
Use this content to understand how indices are defined, calculated, and what they mean.
When the user asks about specific indices (e.g., Innovation, Efficiency), refer to the Blue Book definitions.

When asked to visualize something:
1. Infer the necessary calculation or data transformation.
2. Generate Python code using `pyecharts` to create the visualization.
3. The code MUST assign the final chart object to a variable named `chart`.
4. Do NOT use `chart.render()`, just assign the object.
5. Use the `pyecharts.options` as `opts`.
6. Explain your reasoning briefly before or after the code block.

Available data context structure:
{data_summary}

{kb_context}

Example Output Format:
Here is the analysis of the data based on the Blue Book definitions...

```python
from pyecharts.charts import Bar
from pyecharts import options as opts

c = (
    Bar()
    ...
)
chart = c
```
"""
    data_summary = summarize_data(data_context)

    formatted_system_prompt = system_prompt.replace("{data_summary}", data_summary).replace("{kb_context}", kb_context)

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

def classify_insight(text: str, api_key: Optional[str] = None, base_url: Optional[str] = None, model: Optional[str] = None) -> str:
    """
    Classifies a user insight into one of the 5 Dimensions.
    Returns the dimension name.
    """
    valid_dimensions = [
        "Scale & Growth", "Structure & Entity", "Time & Space",
        "Efficiency & Quality", "Innovation & Integration"
    ]

    api_key, base_url, model = get_api_config(api_key, base_url, model, text)

    if not api_key or OpenAI is None:
        # Mock classification
        if "growth" in text.lower() or "scale" in text.lower(): return "Scale & Growth"
        if "structure" in text.lower() or "company" in text.lower(): return "Structure & Entity"
        if "time" in text.lower() or "space" in text.lower() or "region" in text.lower(): return "Time & Space"
        if "efficiency" in text.lower() or "quality" in text.lower(): return "Efficiency & Quality"
        if "innovation" in text.lower() or "tech" in text.lower(): return "Innovation & Integration"
        return "Scale & Growth" # Default

    client = OpenAI(api_key=api_key, base_url=base_url)

    prompt = f"""
    Classify the following text into one of these 5 dimensions:
    {', '.join(valid_dimensions)}

    Text: "{text}"

    Return ONLY the dimension name.
    """

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        result = response.choices[0].message.content.strip()
        # Basic cleanup to ensure it matches one of the known dimensions
        for dim in valid_dimensions:
            if dim.lower() in result.lower():
                return dim
        return "Scale & Growth" # Fallback
    except Exception as e:
        print(f"Error classifying insight: {e}")
        return "Scale & Growth"

def generate_dimension_insights(data: DataType, dimension: str, api_key: Optional[str] = None, base_url: Optional[str] = None, model: Optional[str] = None) -> str:
    """
    Generates insights for a specific dimension using data and Blue Book knowledge.
    """
    api_key, base_url, model = get_api_config(api_key, base_url, model, f"insight for {dimension}")

    # Get RAG context for this dimension
    kb = _get_kb()
    kb_context = ""
    if kb:
        # Search for the dimension name specifically
        docs = kb.search(dimension, 5)
        for d in docs:
            kb_context += f"--- Section: {d.section} ---\n{d.content}\n"

    if not api_key or OpenAI is None:
        return f"**AI Insight (Mock):** Based on the data, the {dimension} shows a positive trend. (API Key required for real analysis)"

    client = OpenAI(api_key=api_key, base_url=base_url)

    data_summary = summarize_data(data)

    prompt = f"""
    You are an expert analyst for the Low Altitude Economy.
    Analyze the provided data for the dimension: "{dimension}".

    Use the following definitions and context from the Blue Book to guide your analysis:
    {kb_context}

    Data Summary:
    {data_summary}

    Provide 2-3 concise, strategic insights or observations.
    Focus on "what this means" rather than just "what the numbers are".
    Format as a bulleted list.
    """

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating insights: {e}"

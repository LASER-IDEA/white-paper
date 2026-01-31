import sys
import os

# Add src to python path
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

import llm_helper

def main():
    print("Testing LLM Helper...")

    # Mock data
    data = {
        "flights": [100, 120, 130],
        "companies": {"A": 10, "B": 20}
    }

    # 1. Test get_llm_response (Mock mode)
    print("\n1. Testing get_llm_response (should return mock response with KB info)...")
    explanation, code = llm_helper.get_llm_response("Visualize the flight growth", data)
    print(f"Explanation Preview: {explanation[:100]}...")
    if code:
        print("Code generated: Yes")
    else:
        print("Code generated: No")

    # 2. Test classify_insight (Mock mode)
    print("\n2. Testing classify_insight...")
    insight_text = "The efficiency of flight operations has improved significantly."
    dimension = llm_helper.classify_insight(insight_text)
    print(f"Insight: '{insight_text}'")
    print(f"Classified Dimension: {dimension}")

    insight_text = "Market scale is growing rapidly."
    dimension = llm_helper.classify_insight(insight_text)
    print(f"Insight: '{insight_text}'")
    print(f"Classified Dimension: {dimension}")

    # 3. Test generate_dimension_insights (Mock mode)
    print("\n3. Testing generate_dimension_insights...")
    insights = llm_helper.generate_dimension_insights(data, "Efficiency & Quality")
    print(f"Generated Insights: {insights}")

if __name__ == "__main__":
    main()

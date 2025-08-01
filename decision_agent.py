from typing import TypedDict
from langgraph.graph import StateGraph, END

# Step 1: Define the Graph State
class AgentState(TypedDict):
    input_value: int
    evaluation_result: str

# Step 2: Define Node 1 - Evaluate the input number
def evaluate_number(state: AgentState) -> dict:
    input_value = state["input_value"]
    threshold = 50
    if input_value > threshold:
        return {"evaluation_result": "high"}
    else:
        return {"evaluation_result": "low"}

# Step 3: Define Node 2 - Handle high value
def handle_high_value(state: AgentState) -> dict:
    return {"final_message": "The value is high!"}

# Step 4: Define Node 3 - Handle low value
def handle_low_value(state: AgentState) -> dict:
    return {"final_message": "The value is low."}

# Step 5: Initialize the Graph
graph = StateGraph(AgentState)

# Step 6: Add Nodes to the Graph
graph.add_node("evaluator", evaluate_number)
graph.add_node("high_handler", handle_high_value)
graph.add_node("low_handler", handle_low_value)

# Step 7: Set the Entry Point
graph.set_entry_point("evaluator")

# Step 8: Define Router Function for Conditional Edges
def decide_path(state: AgentState) -> str:
    if state["evaluation_result"] == "high":
        return "high_handler"
    else:
        return "low_handler"

# Step 9: Add Conditional Edge from evaluator
graph.add_conditional_edges(
    "evaluator",
    decide_path,
    {
        "high_handler": "high_handler",
        "low_handler": "low_handler",
    }
)

# Step 10: Set Finish Points
graph.add_edge("high_handler", END)
graph.add_edge("low_handler", END)

# Step 11: Compile the Graph
compiled_graph = graph.compile()

if __name__ == "__main__":
    # Step 1: Run the graph with high and low input values
    result_high = compiled_graph.invoke({"input_value": 75})
    result_low = compiled_graph.invoke({"input_value": 25})

    # Step 2: Observe and print the outputs
    print("Result with high input (75):", result_high)
    print("Result with low input (25):", result_low)

    # Step 3: Optional Visualization (if supported)
    try:
        print("\nMermaid Graph Representation:\n")
        print(compiled_graph.get_graph().draw_mermaid())
    except AttributeError:
        print("\nGraph visualization not supported in this environment.")

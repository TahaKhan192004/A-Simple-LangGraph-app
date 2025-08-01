This project uses **LangGraph** to build a simple decision agent. It takes a number as input, checks if it's greater than 50, and returns a message saying whether the value is high or low — using stateful, conditional logic in a graph structure.



## 🧠 Explanation of `AgentState`

The `AgentState` is a `TypedDict` that serves as the **shared memory** across all graph nodes. It allows each node to access and update specific fields in a predictable way:

```python
class AgentState(TypedDict):
    input_value: int
    evaluation_result: str
```

This ensures type-safe, structured data flow through the graph.

---

## ⚙️ Node Functions and Their Roles

| Function            | Role Description                                                                             |
| ------------------- | -------------------------------------------------------------------------------------------- |
| `evaluate_number`   | Reads `input_value` and evaluates it against a threshold (50), updating `evaluation_result`. |
| `handle_high_value` | Adds `final_message` to the state if the value is "high".                                    |
| `handle_low_value`  | Adds `final_message` to the state if the value is "low".                                     |

Each function receives the full `AgentState`, makes a decision, and returns partial updates to be merged into the global state.

---

## 🔀 Conditional Routing with `decide_path`

The `decide_path(state)` function controls **which node runs next** based on the value of `state["evaluation_result"]`. This implements the decision logic of the graph:

```python
def decide_path(state: AgentState) -> str:
    if state["evaluation_result"] == "high":
        return "high_handler"
    else:
        return "low_handler"
```

It allows dynamic branching from a single node (`evaluator`) to one of two others.

---

## 🧪 Final AgentState Outputs

### For input\_value = 75:

```python
{
  "input_value": 75,
  "evaluation_result": "high",
  "final_message": "The value is high!"
}
```

### For input\_value = 25:

```python
{
  "input_value": 25,
  "evaluation_result": "low",
  "final_message": "The value is low."
}
```

---

## 📈 Reflection on LangGraph's Power

This example demonstrates that:

* **LangGraph enables branching logic** based on state, which is hard to express with traditional LangChain chains.
* You can create **clear, readable workflows** without relying on deeply nested logic.
* The `TypedDict` state model makes it easy to trace how data evolves through the graph.
* Adding loops, memory, retries, or complex sub-flows becomes more manageable as graphs grow.

---

## ❗ Challenges & Resolutions

| Challenge                                          | Resolution                                                                                                       |
| -------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `ModuleNotFoundError: No module named 'langgraph'` | Resolved by installing the package using `pip install langgraph`                                                 |
| Unsure how state merging works                     | Understood that each node returns a partial `dict`, and LangGraph merges it into the global state automatically. |
| Visualizing the graph                              | Found that `draw_mermaid()` works if the environment supports Mermaid syntax in output.                          |

---

---

Let me know if you’d like the Markdown file exported, or if you want help expanding this example with more nodes or LangChain integrations.
```

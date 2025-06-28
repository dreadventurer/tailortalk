# langgraph_flow.py

from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
from datetime import datetime

# Step 1: Define shared state
class GraphState(TypedDict):
    input_text: Annotated[str, "User's input"]
    extracted_time: Annotated[str, "Extracted time"]

# Step 2: Define nodes
from dateparser import parse
from dateparser.search import search_dates
import re

def extract_time_node(state: GraphState) -> GraphState:
    text = state['input_text']

    # Search for date/time phrases
    result = search_dates(text, settings={'PREFER_DATES_FROM': 'future'})

    if result:
        # Get the first matched datetime
        dt = result[0][1]
        extracted = dt.strftime("%Y-%m-%d at %I:%M %p")
    else:
        extracted = "unknown"

    return {
        **state,
        "extracted_time": extracted
    }



def print_node(state: GraphState) -> GraphState:
    print(" Extracted Time:", state["extracted_time"])
    return state

# Step 3: Define flow (graph)
graph = StateGraph(GraphState)
graph.add_node("extract_time", extract_time_node)
graph.add_node("print", print_node)

graph.set_entry_point("extract_time")
graph.add_edge("extract_time", "print")
graph.add_edge("print", END)

# Step 4: Compile & run
app = graph.compile()

if __name__ == "__main__":
    input_state = {"input_text": "Schedule call next Tuesday at 11:30 AM"} 
    app.invoke(input_state)

from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    """the state of our graph - a simple example"""
    value: int 
    message: str

def add_ten(state: State) -> dict:
    """ A note that adds 10 to the value. """
    new_value = state['value'] + 10
    return {
        "value": new_value, 
        "message": f"Added 10 to get {new_value}"
    }

def multiply_by_two(state: State) -> dict:
    """ A note that multiplies the value by 2. """
    new_value = state['value'] * 2
    return {
        "value": new_value, 
        "message": f"Multiplied by 2 to get {new_value}"
    }

builder = StateGraph(State)

builder.add_node("add_ten", add_ten)
builder.add_node("multiply_by_two", multiply_by_two)

builder.add_edge(START, "add_ten")
builder.add_edge("add_ten", "multiply_by_two")
builder.add_edge("multiply_by_two", END)

graph = builder.compile()

initial_state = {"value": 5, "message": "Starting value is 5."}

result = graph.invoke(initial_state)

print(f"\nFinal state: {result}")


from typing import Annotated
from operator import add
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END

class AnalysisState(BaseModel):
    """State doe document analysis pipeline"""

    # Input document - no reducer needed, stays constant
    document: str = ""

    # Finding accumulate from each node using the add reducer
    findings: Annotated[list[str], add] = Field(default_factory=list)

    # Status gets overwritten by each node (default behaivor)
    status: str = "pending"


def extract_keywords(state: AnalysisState) -> dict:
    """Extract keywords from the document"""

    doc = state.document.lower()

    keywords_found = []
    keyword_list = ["ai", "machine learning", "data", "python", "automation"]
    for keyword in keyword_list:
        if keyword in doc:
            keywords_found.append(keyword)
    
    return {
        "findings": keywords_found, # will be appended
        "status": "keywords extracted" # will overwrite
    }

def analyze_sentiment(state: AnalysisState) -> dict:
    """Analyze the sentiment of the document"""

    doc = state.document.lower()

    possitive_words = ["good", "great", "excellent", "positive", "happy"]
    negative_words = ["bad", "terrible", "poor", "negative", "sad"]

    positive_count = sum(1 for word in possitive_words if word in doc)
    negative_count = sum(1 for word in negative_words if word in doc)

    if positive_count > negative_count:
        sentiment = "positive"
    elif positive_count < negative_count:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return {
        "findings": [f"sentiment: {sentiment}"], # will be appended
        "status": "sentiment analyzed" # will overwrite
    }

def generate_stats(state: AnalysisState) -> dict:
    """Generate statistics from the document"""

    doc = state.document.lower()

    word_count = len(doc.split())
    sentence_count = doc.count(".") + doc.count("!") + doc.count("?")

    return {
        "findings": [
            f"Word count: {word_count}",
            f"Sentence count: {sentence_count}",
        ],
        "status": "stats generated",
    }

builder = StateGraph(AnalysisState)

builder.add_node("extract_keywords", extract_keywords)
builder.add_node("analyze_sentiment", analyze_sentiment)
builder.add_node("generate_stats", generate_stats)

builder.add_edge(START, "extract_keywords")
builder.add_edge("extract_keywords", "analyze_sentiment")
builder.add_edge("analyze_sentiment", "generate_stats")
builder.add_edge("generate_stats", END)

graph = builder.compile()   

sample_document = """
Artificial Intelligence (AI) is transforming the world. It has applications in various fields such as machine learning, data analysis, and automation. 
Overall,the impact of AI is positive, but there are also concerns about its ethical implications.
"""

result = graph.invoke(AnalysisState(document=sample_document))

# display results
print("DOCUMENT ANALYSIS RESULTS")
print("=========================")
print(f"final status: {result['status']}")
print("findings:")
for finding in result["findings"]:
    print(f"- {finding}")
print("=========================")

from typing import Annotated
from operator import add
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END

class AnalysisState(BaseModel):
    """State for document analysis pipeline"""

    # Input document - no reducer needed, stays constant
    document: str = ""

    # Findings accumulate from each node using the add reducer
    findings: Annotated[list[str], add] = Field(default_factory=list)

    # Status gets overwritten by each node (default behavior)
    status: str = "pending"


def extract_keywords(state: AnalysisState) -> dict:
    """Extract keywords from the document"""

    doc = state.document.lower()

    keywords_found = []
    keyword_list = ["ai", "machine learning", "data", "python", "automation"]
    for keyword in keyword_list:
        if keyword in doc:
            keywords_found.append(f"Keyword found: '{keyword}'")

    return {
        "findings": keywords_found,
        "status": "keywords extracted",
    }

def analyze_sentiment(state: AnalysisState) -> dict:
    """Analyze the sentiment of the document"""

    doc = state.document.lower()

    positive_words = ["good", "great", "excellent", "positive", "happy"]
    negative_words = ["bad", "terrible", "poor", "negative", "sad"]

    positive_count = sum(1 for word in positive_words if word in doc)
    negative_count = sum(1 for word in negative_words if word in doc)

    if positive_count > negative_count:
        sentiment = "Positive"
    elif positive_count < negative_count:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {
        "findings": [f"Sentiment: {sentiment}"],
        "status": "sentiment analyzed",
    }

def generate_stats(state: AnalysisState) -> dict:
    """Generate statistics from the document"""

    doc = state.document

    word_count = len(doc.split())
    sentence_count = doc.count(".") + doc.count("!") + doc.count("?")

    return {
        "findings": [
            f"Word count: {word_count}",
            f"Sentence count: {sentence_count}",
        ],
        "status": "complete",
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

sample_document = (
    "Artificial Intelligence (AI) is rapidly transforming the entire modern world today. "
    "It has many applications in fields such as machine learning, data analysis, and automation. "
    "Python is a popular language widely used in modern AI systems. "
    "Overall, the impact of AI is positive, but concerns about ethical implications exist."
)

result = graph.invoke(AnalysisState(document=sample_document))

# display results
print("=" * 49)
print("DOCUMENT ANALYSIS RESULTS")
print("=" * 49)
print()
print(f"Final Status: {result['status']}")
print()
print("Findings (accumulated from all nodes):")
for i, finding in enumerate(result["findings"], start=1):
    print(f"  {i}. {finding}")

# LangChain Examples

This workspace contains small Python examples that show different LLM patterns with LangChain.

## Files

- [01_weather_tool_agent.py](01_weather_tool_agent.py): Basic tool-calling agent example. Registers a custom weather tool and asks the agent a weather question.
- [02_structured_output.py](02_structured_output.py): Structured output example. Uses a Pydantic model to extract name, age, and email from free text.
- [03_search_agent_tavily.py](03_search_agent_tavily.py): Web-search agent example. Uses Tavily as a tool and asks for an exchange-rate related answer.
- [04_writing_improvement.py](04_writing_improvement.py): Writing improvement chain. Generates a draft paragraph, critiques it, then rewrites it with improvements.
- [05_rag_local_docs.py](05_rag_local_docs.py): Simple RAG chain demo. Retrieves relevant local documents with keyword overlap, then answers using the retrieved context.
- [06_summarization_chain.py](06_summarization_chain.py): Summarization chain demo. Produces a 3-paragraph explanation, a 3-sentence summary, and a tweet-sized version.
- [07_react_fruit_agent.py](07_react_fruit_agent.py): ReAct-style loop demo with fruit price actions and tool observations.

## Notes

- These examples use environment variables loaded from a .env file.
- OPENAI_API_KEY is required for LLM generation.
- Some scripts include fallback messages when the API key is missing.

# LangChain Examples

This workspace contains small Python examples that show different LLM patterns with LangChain.

## Files

- [main.py](main.py): Basic tool-calling agent example. Registers a custom weather tool and asks the agent a weather question.
- [example2.py](example2.py): Structured output example. Uses a Pydantic model to extract name, age, and email from free text.
- [example3.py](example3.py): Web-search agent example. Uses Tavily as a tool and asks for an exchange-rate related answer.
- [example4.py](example4.py): Writing improvement chain. Generates a draft paragraph, critiques it, then rewrites it with improvements.
- [example5.py](example5.py): Simple RAG chain demo. Retrieves relevant local documents with keyword overlap, then answers using the retrieved context.
- [example6.py](example6.py): Summarization chain demo. Produces a 3-paragraph explanation, a 3-sentence summary, and a tweet-sized version.

## Notes

- These examples use environment variables loaded from a .env file.
- OPENAI_API_KEY is required for LLM generation.
- Some scripts include fallback messages when the API key is missing.

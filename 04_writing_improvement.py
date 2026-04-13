from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from dotenv import load_dotenv
from langchain_tavily import TavilySearch

load_dotenv()


base_model = ChatOpenAI(model="gpt-5", temperature=0.1)

# llm_call function with a given topic that calls the model and returns the response
def llm_call(message: str) -> str:
    result = base_model.invoke(message)
    return result.content

def writing_improvement_chain(topic: str) -> str:
    # Step 1: Generate first draft
    draft = llm_call(f"Write a paragraph about {topic}")

    # Step 2: Critique the draft
    critique = llm_call(f"What could be improved?\n{draft}")

    # Step 3: Rewrite with improvements
    final = llm_call(f"Rewrite:\n{draft}\n\nFix:\n{critique}")

    return final


topic = "Bolivia"
print(writing_improvement_chain(topic))


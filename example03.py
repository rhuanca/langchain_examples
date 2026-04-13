from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
load_dotenv()



base_model = ChatOpenAI(model="gpt-5", temperature=0.1)

search_tool = TavilySearch(
    max_results=5,
    search_depth="basic",
    include_raw_content=False,
    include_rax_images=False,
)


agent = create_agent(model=base_model, tools=[search_tool])

def ask_agent(question: str) -> str:
    
    """Ask the agent a question and return the response."""


    result = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": question}
            ]
        }
    )

    print(result)
    return result["messages"][-1].content

final_result = ask_agent("What is the current exchange rate for 1 USD to BOB?")


print("Final result:\n\n-----------------------------------------------\n", final_result)



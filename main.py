from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool


load_dotenv()


model  = ChatOpenAI(model="gpt-5", temperature=0.1)

@tool
def get_weather(city: str) -> str:
    """
    Retrieve weather information for a specified city.
    Args:
        city (str): The name of the city to get weather data for.
    Returns:
        str: A string containing the weather conditions and temperature for the city,
             or a message indicating that weather data is not available if the city
             is not found in the database.
    Example:
        >>> get_weather("New York")
        'Sunny, 25°C'
        >>> get_weather("Unknown City")
        'Weather data not available for this city.'
    """
    
    weather_data = {
        "New York": "Sunny, 25°C",
        "Los Angeles": "Cloudy, 20°C",
        "Chicago": "Rainy, 15°C",
        "Houston": "Windy, 30°C",
        "Phoenix": "Hot, 35°C"
    }
    return weather_data.get(city, "Weather data not available for this city.")


agent = create_agent(model=model, tools=[get_weather])

def ask_agent(question: str) -> str:
    
    """Ask the agent a question and return the response."""


    result = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": question}
            ]
        }
    )

    return result["messages"][-1].content


print(ask_agent("What is the weather in La Paz?"))



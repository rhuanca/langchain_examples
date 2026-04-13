from openai import OpenAI
import re

from dotenv import load_dotenv

_ = load_dotenv()

client = OpenAI()


class Agent:
    """
    A class representing an AI agent that can engage in conversations using OpenAI's API.

    """

    def __init__(self, system=""):
        """
        Initialize the Agent with an optional system message.

        Args:
            system (str): The system message to set the context for the agent.
        """
        

        self.system = system
        self.messages = []

        if self.system:
            self.messages.append({"role": "system", "content": self.system})
    

    def __call__(self, message):
        """
        Allow the agent to be called directly with a message

        Args:
            message (str): The user's input message.

        Returns:
            str: The agent's response to the input message.    
        """
        self.messages.append({"role": "user", "content": message})

        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result
    
    def execute(self):
        """
        Execute the conversation by sending the entire conversation history to the OpenAI API.

        Returns:
            str: The content of the model's response.
        """

        completion = client.chat.completions.create(
            model="gpt-5.4-mini",
            temperature=0,
            messages=self.messages
        )
        return completion.choices[0].message.content


prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer.
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

calculate_total_price:
e.g. calculate_total_price: apple: 2, banana: 3
Runs a calculation for the total price based on the quantity and prices of the fruits.

get_fruit_price:
e.g. get_fruit_price: apple
returns the price of the fruit when given its name.


Example session:

Question: What is the total price for 2 apples and 3 bananas?
Thought: I should calculate the total price by getting the price of each fruit and summing them up.
Action: get_fruit_price: apple
PAUSE

Observation: The price of an apple is $1.5.

Action: get_fruit_price: banana
PAUSE

Observation: The price of a banana is $1.2.

Action: calculate_total_price: apple: 2, banana: 3
PAUSE

You then output:

Answer: The total price for 2 apples and 3 bananas is $6.6.

""".strip()

fruit_prices = {
    "apple": 1.5,
    "banana": 1.2,
    "orange": 1.3,
    "grapes": 2.0
}



# Function to calcualte the price of a specific fruit
def get_fruit_price(fruit: str) -> str:
    price = fruit_prices.get(fruit.lower())
    if price is not None:
        return f"The price of a {fruit} is ${price}."
    else:
        return f"Sorry, I don't have the price for {fruit}."
    
# Function to calculate total price based on quantities.
def calculate_total_price(fruits: str) -> str:
    total = 0.0
    for item in fruits.split(","):
        fruit, quantity = item.split(":")
        fruit = fruit.strip()
        quantity = int(quantity.strip())
        price = fruit_prices.get(fruit.lower())
        if price is not None:
            total += price * quantity
        else:
            return f"Sorry, I don't have the price for {fruit}."
    return f"The total price for {fruits} is ${total}."    

# Mapping actions to functions
knows_actions = {
    "get_fruit_price": get_fruit_price,
    "calculate_total_price": calculate_total_price
}


action_re = re.compile(r'^Action: (\w+): (.*)$')

def query(question):
    bot = Agent(prompt)
    result = bot(question) #__call__
    print("-----")
    print(result)
    print("-----")
    actions = [
        action_re.match(line) 
        for line in result.splitlines() if action_re.match(line)
    ]

    if actions:
        action, action_input = actions[0].groups()
        if action not in knows_actions:
            raise ValueError(f"Unknown action: {action}: {action_input}")
        print(f"Running action: {action} with input: {action_input}")
        observation = knows_actions[action](action_input)
        print(f"Observation: {observation}")
    else:
        return


query("what is the price of orange?")
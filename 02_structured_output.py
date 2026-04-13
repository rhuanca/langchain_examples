from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()


class UserInfo(BaseModel):
    name: str = Field(description="The user's name")
    age: int = Field(description="The user's age")
    email: Optional[str] = Field(description="The user's email address")

base_model = ChatOpenAI(model="gpt-5", temperature=0)


structured_model = base_model.with_structured_output(UserInfo)


user_text = "Extract the user's name, age, and email from the following text: 'My name is John Doe, I am 30 years old, and my email is john.doe@example.com'"
print("User text:", user_text)

result = structured_model.invoke(user_text)

print(result)



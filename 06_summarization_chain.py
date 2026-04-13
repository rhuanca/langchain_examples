from __future__ import annotations

import os
from typing import Dict

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


def llm_call(message: str) -> str:
    """Call the chat model with a plain string prompt."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "OPENAI_API_KEY is not set. LLM generation is skipped."

    model = ChatOpenAI(model="gpt-5", temperature=0.1)
    result = model.invoke(message)
    return result.content


def summarization_chain(topic: str) -> Dict[str, str]:
    """
    Build a 3-step summarization chain.

    Returns:
        A dictionary with keys:
        - "explanation": A detailed 3-paragraph explanation of the topic
        - "summary": A 3-sentence summary of the explanation
        - "tweet": A single tweet (280 chars or less) condensing the summary
    """
    # TODO 1: Generate a detailed explanation of the topic using llm_call()
    #         Ask for exactly 3 paragraphs
    #         Store the result in a variable called 'explanation'
    explanation_prompt = (
        f"Explain the topic '{topic}' in exactly 3 paragraphs. "
        "Keep it factual, clear, and easy to understand."
    )
    explanation = llm_call(explanation_prompt)

    # TODO 2: Summarize the explanation to exactly 3 sentences using llm_call()
    #         Pass the explanation from step 1 to the prompt
    #         Store the result in a variable called 'summary'
    summary_prompt = (
        "Summarize the text below in exactly 3 sentences.\n\n"
        f"Text:\n{explanation}"
    )
    summary = llm_call(summary_prompt)

    # TODO 3: Condense the summary to a tweet using llm_call()
    #         Pass the summary from step 2 to the prompt
    #         Ask for exactly 280 characters or less
    #         Store the result in a variable called 'tweet'
    tweet_prompt = (
        "Turn the summary below into one tweet of 280 characters or less. "
        "Do not use hashtags unless needed.\n\n"
        f"Summary:\n{summary}"
    )
    tweet = llm_call(tweet_prompt)

    # Hard guard so the output always fits a tweet.
    if len(tweet) > 280:
        tweet = tweet[:277] + "..."

    return {
        "explanation": explanation,
        "summary": summary,
        "tweet": tweet,
    }


if __name__ == "__main__":
    topic = "Bolivia"
    result = summarization_chain(topic)

    print("Topic:", topic)
    print("\nExplanation:\n")
    print(result["explanation"])
    print("\nSummary:\n")
    print(result["summary"])
    print("\nTweet:\n")
    print(result["tweet"])

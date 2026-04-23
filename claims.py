import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    azure_endpoint=os.getenv("OPENAI_ENDPOINT"),
    api_version=os.getenv("OPENAI_API_VERSION")
)

deployment = os.getenv("OPENAI_DEPLOYMENT")


def extract_claims(text):
    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {
                "role": "system",
                "content": (
                    "You extract factual, verifiable claims from text. "
                    "Return ONLY valid JSON as a list of objects with keys: claim and checkable."
                )
            },
            {
                "role": "user",
                "content": f"""
Extract the factual claims from this text:

{text}

Return JSON exactly like:
[
  {{"claim": "The Earth is flat.", "checkable": true}},
  {{"claim": "The Earth orbits the Sun.", "checkable": true}}
]
"""
            }
        ],
        temperature=0
    )

    answer = response.choices[0].message.content.strip()

    start = answer.find("[")
    end = answer.rfind("]")

    if start != -1 and end != -1:
        return json.loads(answer[start:end+1])

    return []
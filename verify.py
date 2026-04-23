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


def verify_claims(claims):
    results = []

    for item in claims:
        claim_text = item.get("claim") if isinstance(item, dict) else str(item)

        if not claim_text or not claim_text.strip():
            continue

        try:
            response = client.chat.completions.create(
                model=deployment,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a fact-checking AI. "
                            "Return ONLY valid JSON with keys: "
                            "claim, verdict, confidence, highlight_red, explanation. "
                            "Verdict must be one of: Supported, Contradicted, Unverifiable."
                        )
                    },
                    {
                        "role": "user",
                        "content": f"""
Fact check this claim:

{claim_text}

Return JSON exactly like this:
{{
  "claim": "{claim_text}",
  "verdict": "Supported",
  "confidence": 0.95,
  "highlight_red": false,
  "explanation": "Short explanation here."
}}
"""
                    }
                ],
                temperature=0
            )

            answer = response.choices[0].message.content.strip()

            start = answer.find("{")
            end = answer.rfind("}")

            if start != -1 and end != -1:
                parsed = json.loads(answer[start:end+1])
                results.append(parsed)
            else:
                results.append({
                    "claim": claim_text,
                    "verdict": "Unverifiable",
                    "confidence": 0.0,
                    "highlight_red": False,
                    "explanation": answer
                })

        except Exception as e:
            results.append({
                "claim": claim_text,
                "verdict": "Error",
                "confidence": 0,
                "highlight_red": False,
                "explanation": str(e)
            })

    return results
from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from openai import OpenAI
from dotenv import load_dotenv
import json
import time

load_dotenv(".env")
client = OpenAI()

app = FastAPI()

with open("system_prompt.txt", 'r') as file:
    system_prompt = file.read()


@app.get("/chat/with_hc")
def chat_with_hc(query: str = Query(..., description="User query for step-by-step reasoning")):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]

    def generate():
        while True:
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    response_format={"type": "json_object"},
                    messages=messages
                )

                content = response.choices[0].message.content
                parsed = json.loads(content)

                step = parsed.get("step", "")
                explanation = parsed.get("content", "")

                yield f"\n➡️ {explanation}\n"

                messages.append({"role": "assistant", "content": json.dumps(parsed)})
                if step.lower() == "result":
                    break
                time.sleep(0.3)

            except Exception as e:
                yield f"\n❌ Error: {str(e)}\n"
                break

    return StreamingResponse(generate(), media_type="text/plain")

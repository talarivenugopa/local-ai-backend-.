import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

# Render ఎన్విరాన్‌మెంట్ నుండి API keyని తీసుకుంటుంది
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_text(request: PromptRequest):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": request.prompt,
                }
            ],
          model="llama-3.1-8b-instant",  
        )
        return {"response": chat_completion.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

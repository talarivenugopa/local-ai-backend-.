from fastapi import FastAPI
import httpx
import sqlite3

app = FastAPI()

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY AUTOINCREMENT, prompt TEXT, response TEXT)")
    conn.commit()
    conn.close()

init_db()

@app.get("/")
def read_root():
    return {"message": "Local AI Backend is running with Ollama & SQLite!"}

@app.post("/generate")
async def generate_text(prompt: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3", "prompt": prompt, "stream": False},
            timeout=60.0
        )
        res_data = response.json()
        ai_response = res_data.get("response", "")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (prompt, response) VALUES (?, ?)", (prompt, ai_response))
    conn.commit()
    conn.close()

    return {"prompt": prompt, "response": ai_response}

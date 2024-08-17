from fastapi import FastAPI
import uvicorn
import time

from database import generate_client, create_openai_client, prompt
from keywords import find_keywords
import settings

app = FastAPI()

message_history = [{"role": "system", "content": settings.LLM_PROMPT_SHELL},]

@app.get('/api/message')
def route(message: str = "Hello!"):
    global message_history # bad style, move to sqlite
    keywords = find_keywords(message, settings.KEYWORD_LIMIT)
    model_response, updated_history = prompt(generate_client(), create_openai_client(), message, keywords, message_history)

    message_history = updated_history

    return {"message": model_response}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
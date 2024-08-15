from fastapi import FastAPI
import uvicorn
import time

from database import generate_client, prompt
from keywords import find_keywords
import settings

app = FastAPI()

@app.get('/api/message')
def route(message: str = "Hello!"):
    keywords = find_keywords(message, settings.KEYWORD_LIMIT)
    model_response = prompt(generate_client(), settings.LLM_PROMPT_SHELL + message, keywords)

    return {"message": model_response.generated}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
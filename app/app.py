from fastapi import FastAPI
import uvicorn
import time

app = FastAPI()

@app.get('/api/message')
def route(message: str = "Hello!"):
    return {'message': message}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
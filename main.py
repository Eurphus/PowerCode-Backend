from fastapi import FastAPI
from verify import run_test_cases
from pydantic import BaseModel


class code_request(BaseModel):
    code: str
    user_id: int


class user_request(BaseModel):
    user1: int
    user2: int


app = FastAPI()


@app.get("/api/message")
async def root():
    return {"message": "World"}


@app.get("api/challenges/{language}")
async def get_challenges(language: str, request: user_request):
    return {}


@app.post("/api/code-check/{language}/{challenge}")
async def verify_code(language: str, challenge: str, request: code_request):
    print("FOUND: " + challenge)
    response = run_test_cases(request.code, language, challenge)
    return response

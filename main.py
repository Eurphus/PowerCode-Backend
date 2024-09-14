from fastapi import FastAPI
from verify import run_test_cases
from pydantic import BaseModel

class code_request(BaseModel):
    code: str
    user_id: int

app = FastAPI()

@app.get("/api/message")
async def root():
    return {"message": "World"}

@app.post("/api/code-check/{challenge}")
async def verify_code(challenge: str, request: code_request):
    print("FOUND: " + challenge)
    response = run_test_cases(request.code, challenge)
    return {
        "success": response[0],
        "tests": response[1]
    }

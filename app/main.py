from fastapi import FastAPI, HTTPException
from app.utils.exec import run_test_cases
from app.utils.info import challenge_data
from app.models import CodeRequest, UserScoreRequest
from random import choice
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)

@app.get("/api/message")
async def root():
    return {"message": "World"}

@app.get("/api/details/all")
async def get_all_details():
    return challenge_data

@app.get("/api/match/{language}")
async def match_users(language: str, request: UserScoreRequest):
    if language not in challenge_data:
        raise HTTPException(404, detail="Please include a valid language")

    avg = (request.user_score_1 + request.user_score_2) // 2000
    match = challenge_data[language][choice(list(challenge_data[language]))]
    print(match)

    return match

@app.get("/api/details/{language}/{challenge}")
async def get_details(language: str, challenge: str):
    if not challenge and not language:
        raise HTTPException(404, detail="Please include a language and challenge")
    elif language not in challenge_data:
        raise HTTPException(404, detail="Please include a valid language")
    elif challenge not in challenge_data[language]:
        raise HTTPException(404, detail="Please include a valid challenge")

    return challenge_data[language][challenge]


@app.get("/api/code-check/{language}/{challenge}")
async def verify_code(language: str, challenge: str, request: CodeRequest):
    if not challenge and not language:
        raise HTTPException(404, detail="Please include a language and challenge")
    elif language not in challenge_data:
        raise HTTPException(404, detail="Please include a valid language")
    elif challenge not in challenge_data[language]:
        raise HTTPException(404, detail="Please include a valid challenge")

    print("FOUND: " + challenge)
    response = run_test_cases(request.code, language, challenge)
    return response

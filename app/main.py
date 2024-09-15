from fastapi import FastAPI, HTTPException
from app.utils.exec import run_test_cases
from app.utils.info import challenge_data
from app.models import CodeRequest
from random import choice
from app.utils import dockerize as dockerize
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"]
)


@app.get("/api/message")
async def root():
    return {"message": "World"}


@app.get("/api/details/all")
async def get_all_details():
    return challenge_data


@app.get("/api/match/{language}")
async def match_users(language: str):
    if language not in challenge_data:
        raise HTTPException(404, detail="Please include a valid language")

    # avg = (request.user_score_1 + request.user_score_2) // 2000
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


@app.post("/api/code-check/{language}/{challenge}")
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


@app.post("/api/init-game/{language}/{challenge}")
async def init_game(language: str, challenge: str, user_id_1: int, user_id_2: int):
    container_1 = dockerize.init_docker(language, challenge, user_id_1)
    container_2 = dockerize.init_docker(language, challenge, user_id_2)

    return {
        "success": 0,
        "user_1_container": container_1[0],
        "user_1_dir": container_1[1],
        "user_2_container": container_2[0],
        "user_2_dir": container_2[1],
    }

from pydantic import BaseModel


class CodeRequest(BaseModel):
    code: str
    user_id: int


class UserScoreRequest(BaseModel):
    user_score_1: int
    user_score_2: int

from pydantic import BaseModel


class CodeRequest(BaseModel):
    code: str
    user_id: int


class UserRequest(BaseModel):
    user1: int
    user2: int

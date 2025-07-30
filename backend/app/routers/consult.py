from fastapi import APIRouter, Depends
from pydantic import BaseModel
from ..auth import get_current_user, User
from ..openai_client import chat_completion
from ..nasa import search_techport

class ConsultRequest(BaseModel):
    query: str

consult_router = APIRouter()

@consult_router.post("/consult")
async def consult(body: ConsultRequest, _: User = Depends(get_current_user)):
    nasa_info = await search_techport(body.query)
    answer = await chat_completion(f"With the following NASA data: {nasa_info}\nAnswer: {body.query}")
    return {"answer": answer, "source": "NASA TechPort + GPT-4"}

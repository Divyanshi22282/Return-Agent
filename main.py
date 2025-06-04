# app/main.py

from fastapi import FastAPI
from app.database.connection import init_db
from app.services.return_handler import return_request, ChatInput
from app.services.rule_policy import process_return_policy_change
from pydantic import BaseModel
app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.post("/return-request")
async def handle_return_request(chat: ChatInput):
    return await return_request(chat)



class PromptRequest(BaseModel):
    prompt: str


@app.post("/update-return-policy")
async def update_return_policy(request: PromptRequest):
    result = await process_return_policy_change(request.prompt)
    return result

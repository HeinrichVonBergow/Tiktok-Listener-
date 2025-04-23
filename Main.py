from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from TikTokApi import TikTokApi

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserRequest(BaseModel):
    username: str

@app.get("/")
def root():
    return {"message": "TikTok Listener Backend läuft"}

@app.post("/api/user")
async def get_user(req: UserRequest):
    try:
        async with TikTokApi() as api:
            user = await api.user(username=req.username)
            return {
                "nickname": user.nickname,
                "user_id": user.id,
                "live": user.is_live
            }
    except Exception as e:
        return {"error": str(e)}

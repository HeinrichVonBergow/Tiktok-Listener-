from fastapi import FastAPI
from pydantic import BaseModel
from TikTokApi import TikTokApi

app = FastAPI()

class UserRequest(BaseModel):
    username: str

@app.post("/api/user")
async def get_user_data(request: UserRequest):
    try:
        api = TikTokApi()
        user = api.user(request.username)
        return {
            "nickname": user.get("user", {}).get("nickname", ""),
            "user_id": user.get("user", {}).get("id", ""),
            "live": "live_data" in user
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
async def root():
    return {"message": "TikTok Listener Backend läuft"}
  

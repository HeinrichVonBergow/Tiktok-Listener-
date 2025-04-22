from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from TikTokApi import TikTokApi

app = FastAPI()

# CORS Einstellungen für Zugriff von Vercel etc.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "TikTok Listener Backend läuft"}

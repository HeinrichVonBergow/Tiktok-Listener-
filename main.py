from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from TikTokApi import TikTokApi

app = FastAPI()

# CORS für Vercel erlauben
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modell für eingehende JSON-Daten
class UserRequest(BaseModel):
    username: str

@app.get("/")
def read_root():
    return {"message": "TikTok Listener Backend läuft"}

@app.post("/api/user")
async def get_user_info(req: UserRequest):
    try:
        async with TikTokApi() as api:
            user_data = await api.user(username=req.username)
            return {
                "nickname": user_data.nickname,
                "user_id": user_data.id,
                "live": user_data.is_live
            }
    except Exception as e:
        return {"error": str(e)}

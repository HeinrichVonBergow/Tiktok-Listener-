# backend/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

class UserRequest(BaseModel):
    username: str

@app.get("/")
def root():
    return {"message": "TikTok Listener Backend via Apify läuft"}

@app.post("/api/user")
def get_user(req: UserRequest):
    api_url = "https://api.apify.com/v2/acts/apify~tiktok-profile-scraper/run-sync-get-dataset-items"
    headers = {"Content-Type": "application/json"}
    payload = {"search": req.username}
    params = {"token": "apify_api_C70DLbFacqO0FAlJusY3LohKaqmSgc0xocLR"}

    try:
        response = requests.post(api_url, headers=headers, params=params, json=payload)
        response.raise_for_status()
        data = response.json()

        if not data:
            raise HTTPException(status_code=404, detail="User not found")

        user_data = data[0]
        return {
            "nickname": user_data.get("nickname"),
            "user_id": user_data.get("userId"),
            "live": user_data.get("isLive", False)
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"API request failed: {str(e)}")

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from apify_client import ApifyClient

app = FastAPI()

class UserRequest(BaseModel):
    username: str

@app.post("/api/user")
def get_user(req: UserRequest):
    client = ApifyClient("apify_api_C70DLbFacqO0FAlJusY3LohKaqmSgc0xocLR")
    run_input = {
        "search": req.username
    }
    try:
        run = client.actor("apify/tiktok-profile-scraper").call(run_input=run_input)
        dataset_items = client.dataset(run["defaultDatasetId"]).list_items().items
        if not dataset_items:
            raise HTTPException(status_code=404, detail="User not found")
        user_data = dataset_items[0]
        return {
            "nickname": user_data.get("nickname"),
            "user_id": user_data.get("userId"),
            "live": user_data.get("isLive")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

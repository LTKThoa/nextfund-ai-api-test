from fastapi import FastAPI
from app.schemas import CampaignRequest
from app.moderation import moderate_campaign

app = FastAPI(
    title="NextFund AI Moderation API"
)

@app.get("/")
def root():
    return {
        "message": "API Running"
    }

@app.post("/moderate")
def moderate(data: CampaignRequest):

    result = moderate_campaign(
        data.title,
        data.description,
        data.goalAmount
    )

    return result
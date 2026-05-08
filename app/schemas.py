from pydantic import BaseModel

class CampaignRequest(BaseModel):
    title: str
    description: str
    goalAmount: float
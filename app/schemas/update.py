from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UpdateCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=255)
    contents: str = Field(..., min_length=1)


class UpdateResponse(BaseModel):
    id: int
    campaign_id: int
    title: str
    contents: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


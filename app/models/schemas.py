from pydantic import BaseModel
from typing import Optional, List


class ChatRequest(BaseModel):
    session_id: str
    message: str


class Recommendation(BaseModel):
    name: str
    duration: Optional[str] = None
    test_type: Optional[str] = None
    url: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    recommendations: Optional[List[Recommendation]] = None
    end_of_conversation: bool
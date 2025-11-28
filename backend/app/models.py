from pydantic import BaseModel
from typing import List, Optional

class ChatQuery(BaseModel):
    user_id: str
    text: str
    context: Optional[dict] = None

class Product(BaseModel):
    item_id: str
    name: str
    store_id: str
    price: float
    description: str
    category: str

class ChatResponse(BaseModel):
    response_text: str
    action: str  # e.g., 'recommend', 'show-chart', 'navigate'
    data: Optional[List[Product] | dict] = None

class Forecast(BaseModel):
    ds: List[str] # Dates
    yhat: List[float] # Forecasted values
    yhat_lower: List[float]
    yhat_upper: List[float]

class OwnerInsight(BaseModel):
    kpi: str
    value: str
    recommendation: str
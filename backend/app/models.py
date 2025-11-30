from pydantic import BaseModel
from typing import List, Optional, Union

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
    action: str  # e.g., 'recommend', 'show-chart', 'navigate', 'clarify'
    data: Optional[Union[List[Product], dict, List[dict]]] = None

class Forecast(BaseModel):
    ds: List[str] # Dates
    yhat: List[float] # Forecasted values
    yhat_lower: List[float]
    yhat_upper: List[float]

class OwnerInsight(BaseModel):
    kpi: str
    value: str
    recommendation: str

class MarketBasketRule(BaseModel):
    pair: str
    support: float
    confidence: float
    lift: float

class CustomerSegment(BaseModel):
    cluster: int
    segment_name: str
    total_spend: float
    avg_txn_value: float
    frequency: float
    customer_count: int

class CustomerInsight(BaseModel):
    total_spend: float
    visit_count: int
    favorite_store: str
    purchase_probability: float
    persona: str

class SeasonalAnalysis(BaseModel):
    month: str
    total_price: float

class TimeHabits(BaseModel):
    daily_sales: List[dict]
    hourly_sales: List[dict]

class SentimentAnalysis(BaseModel):
    sentiment: str
    count: int

class PersonaAnalysis(BaseModel):
    persona: str
    avg_spend: float
    txn_count: int

class Recommendation(BaseModel):
    item_id: str
    name: str
    price: float
    sales_count: Optional[int] = None
    reason: str
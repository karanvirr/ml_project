from fastapi import APIRouter, HTTPException
from models import ChatQuery, ChatResponse, Product, Forecast, OwnerInsight
import pandas as pd
from prophet import Prophet
from datetime import datetime
from typing import List

router = APIRouter()

# --- Dummy Data Loading ---
# In a real app, this would be a DB connection
try:
    items_df = pd.read_csv("data/items.csv")
    stores_df = pd.read_csv("data/stores.csv")
    transactions_df = pd.read_csv("data/transactions.csv")
    transactions_df['timestamp'] = pd.to_datetime(transactions_df['timestamp'])
except FileNotFoundError:
    print("WARNING: Data files not found. API endpoints may fail.")
    items_df = pd.DataFrame()
    transactions_df = pd.DataFrame()


# --- Shopper Endpoints ---

@router.post("/chat/query", response_model=ChatResponse)
async def chat_query(query: ChatQuery):
    """
    MVP: Simple keyword-based intent detection and retrieval.
    """
    query_text = query.text.lower()
    
    # 1. Simple Intent Detection
    if "shoes" in query_text or "running" in query_text:
        # 2. Simple Retrieval (Content-Based)
        results = items_df[items_df['name'].str.contains("Shoes", case=False)]
        products = results.to_dict('records')
        
        return ChatResponse(
            response_text=f"Found {len(products)} running shoes for you:",
            action="recommend",
            data=products
        )
    
    if "find" in query_text or "where" in query_text:
        return ChatResponse(
            response_text="I can help you find stores! What are you looking for?",
            action="navigate",
            data={}
        )

    return ChatResponse(
        response_text="Sorry, I'm not sure how to help with that yet.",
        action="clarify",
        data={}
    )

@router.get("/catalog/search", response_model=List[Product])
async def search_catalog(q: str):
    """
    Simple keyword search.
    """
    results = items_df[items_df['name'].str.contains(q, case=False) | 
                       items_df['description'].str.contains(q, case=False)]
    return results.to_dict('records')


# --- Business Owner Endpoints ---

@router.get("/stores/{store_id}/forecast", response_model=Forecast)
async def get_store_forecast(store_id: str, horizon: int = 7):
    """
    Generates a simple Prophet forecast for a given store.
    """
    if transactions_df.empty:
        raise HTTPException(status_code=404, detail="Transaction data not loaded")

    store_sales = transactions_df[transactions_df['store_id'] == store_id]
    if store_sales.empty:
        raise HTTPException(status_code=404, detail="No sales data for this store.")

    # Aggregate sales by day
    daily_sales = store_sales.set_index('timestamp').resample('D')['total_price'].sum().reset_index()
    daily_sales = daily_sales.rename(columns={'timestamp': 'ds', 'total_price': 'y'})

    # Fit Prophet model
    m = Prophet(daily_seasonality=False, weekly_seasonality=True)
    m.fit(daily_sales)
    
    # Make forecast
    future = m.make_future_dataframe(periods=horizon)
    forecast_df = m.predict(future)
    
    # Return forecast data
    forecast_data = forecast_df.tail(horizon)
    return {
        "ds": forecast_data['ds'].dt.strftime('%Y-%m-%d').tolist(),
        "yhat": forecast_data['yhat'].tolist(),
        "yhat_lower": forecast_data['yhat_lower'].tolist(),
        "yhat_upper": forecast_data['yhat_upper'].tolist()
    }

@router.get("/owner/{store_id}/insights", response_model=List[OwnerInsight])
async def get_owner_insights(store_id: str):
    """
    Generates simple business insights and stock alerts.
    """
    # 1. KPI: Total Sales (Last 7 days)
    seven_days_ago = datetime.now() - pd.Timedelta(days=7)
    store_sales = transactions_df[
        (transactions_df['store_id'] == store_id) &
        (transactions_df['timestamp'] >= seven_days_ago)
    ]
    total_sales = store_sales['total_price'].sum()
    
    # 2. Recommendation: Stockout Alert (Dummy logic)
    # In reality, this would use the inventory model
    stockout_item = items_df[items_df['store_id'] == store_id].sample(1).iloc[0]['name']

    return [
        OwnerInsight(
            kpi="Last 7 Day Sales",
            value=f"₹{total_sales:,.2f}",
            recommendation="Sales are steady. Consider a weekend promotion."
        ),
        OwnerInsight(
            kpi="Inventory Alert",
            value=f"Low stock: {stockout_item}",
            recommendation="Risk of stockout in 3 days. Reorder 20 units."
        )
    ]
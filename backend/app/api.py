from fastapi import APIRouter, HTTPException
from .models import (
    ChatQuery, ChatResponse, Product, Forecast, OwnerInsight,
    MarketBasketRule, CustomerSegment, CustomerInsight,
    SeasonalAnalysis, TimeHabits, SentimentAnalysis, PersonaAnalysis
)
import pandas as pd
from prophet import Prophet
from datetime import datetime
from typing import List
from .ml.search_engine import ProductSearchEngine
from .ml.analytics import MallAnalytics
from pathlib import Path
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

router = APIRouter()

# Get the directory containing this file (app/)
CURRENT_DIR = Path(__file__).resolve().parent
# Get the parent directory (backend/ or /app in Docker)
BACKEND_DIR = CURRENT_DIR.parent

# Robustly find the data directory
if (BACKEND_DIR / "data").exists():
    # Docker environment: /app/data
    DATA_DIR = BACKEND_DIR / "data"
elif (BACKEND_DIR.parent / "data").exists():
    # Local environment: .../ai mall project/data
    DATA_DIR = BACKEND_DIR.parent / "data"
else:
    # Fallback
    DATA_DIR = BACKEND_DIR / "data"
    print(f"WARNING: Could not find data directory. Defaulting to {DATA_DIR}")

print(f"Using DATA_DIR: {DATA_DIR}")

# --- Data Loading ---
try:
    items_df = pd.read_csv(DATA_DIR / "items.csv")
    stores_df = pd.read_csv(DATA_DIR / "stores.csv")
    transactions_df = pd.read_csv(DATA_DIR / "transactions.csv")
    transactions_df['timestamp'] = pd.to_datetime(transactions_df['timestamp'])
    
    # Load Customers
    customers_path = DATA_DIR / "customers.csv"
    if customers_path.exists():
        customers_df = pd.read_csv(customers_path)
    else:
        customers_df = pd.DataFrame()
        print("WARNING: customers.csv not found.")

    # Load Reviews (New)
    reviews_path = DATA_DIR / "reviews.csv"
    if reviews_path.exists():
        reviews_df = pd.read_csv(reviews_path)
    else:
        reviews_df = pd.DataFrame()
        print("WARNING: reviews.csv not found.")

    # Initialize Engines
    search_engine = ProductSearchEngine(str(DATA_DIR / "items.csv"))
    analytics_engine = MallAnalytics(transactions_df, customers_df, items_df, reviews_df)
    
except FileNotFoundError as e:
    print(f"WARNING: Data files not found at {DATA_DIR}. Error: {e}")
    items_df = pd.DataFrame()
    transactions_df = pd.DataFrame()
    customers_df = pd.DataFrame()
    reviews_df = pd.DataFrame()
    search_engine = None
    analytics_engine = None


# --- Gemini API Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
gemini_model = None

if GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here":
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        # Initialize with minimal safety restrictions for shopping queries
        gemini_model = genai.GenerativeModel('gemini-flash-latest')
        print("✓ Gemini API initialized successfully")
    except Exception as e:
        print(f"WARNING: Failed to initialize Gemini API: {e}")
        gemini_model = None
else:
    print("WARNING: GEMINI_API_KEY not found in environment. Chat will use basic search only.")


def get_mall_context():
    """Generate context about available products and stores for Gemini."""
    if items_df.empty:
        return "No product data available."
    
    # Get unique categories and sample products
    categories = items_df['category'].unique().tolist() if 'category' in items_df.columns else []
    total_products = len(items_df)
    
    # Get top 5 products by store frequency (most available)
    popular_items = items_df['name'].value_counts().head(5).index.tolist() if 'name' in items_df.columns else []
    
    context = f"""
Mall Information:
- Total Products: {total_products}
- Categories Available: {', '.join(categories[:10])}
- Popular Items: {', '.join(popular_items)}
"""
    return context


def create_shopping_assistant_prompt(user_query: str, mall_context: str) -> str:
    """Create a focused prompt for the shopping assistant."""
    return f"""You are an AI shopping assistant for an AI-powered mall. Your ONLY purpose is to help customers with shopping-related queries.

{mall_context}

RULES:
1. ONLY respond to queries about: products, shopping, stores, prices, recommendations, categories, items to buy, gift ideas, fashion, electronics, etc.
2. If asked about anything NOT related to shopping (weather, general knowledge, math, coding, politics, etc.), politely decline with: "I'm a shopping assistant and can only help with product recommendations, store information, and shopping queries. How can I help you find what you're looking for?"
3. Be helpful, friendly, and concise
4. Recommend specific products from the available categories when relevant
5. If the user asks for a product not in our categories, suggest similar alternatives

User Query: {user_query}

Provide a helpful, focused response (max 3 sentences):"""


# --- Shopper Endpoints ---

@router.post("/chat/query", response_model=ChatResponse)
async def chat_query(query: ChatQuery):
    """
    Gemini-powered AI shopping assistant with contextual understanding.
    Falls back to TF-IDF search if Gemini is unavailable.
    """
    query_text = query.text.strip()
    
    # Try Gemini first for intelligent, context-aware responses
    if gemini_model:
        try:
            mall_context = get_mall_context()
            prompt = create_shopping_assistant_prompt(query_text, mall_context)
            
            response = gemini_model.generate_content(prompt)
            ai_response = response.text.strip()
            
            # Check if Gemini declined (off-topic query)
            if "shopping assistant" in ai_response.lower() and "only help with" in ai_response.lower():
                return ChatResponse(
                    response_text=ai_response,
                    action="clarify",
                    data={}
                )
            
            # Get product recommendations using search engine
            products = []
            if search_engine:
                products = search_engine.search(query_text, top_k=6)
            
            # Determine action based on response and products
            action = "recommend" if products else "inform"
            
            return ChatResponse(
                response_text=ai_response,
                action=action,
                data=products if products else {}
            )
            
        except Exception as e:
            print(f"Gemini API error: {e}")
            # Fall through to fallback search
    
    # Fallback: Use TF-IDF search engine
    if search_engine:
        results = search_engine.search(query_text, top_k=6)
        
        if results:
            return ChatResponse(
                response_text=f"Found {len(results)} items matching '{query_text}':",
                action="recommend",
                data=results
            )
    
    return ChatResponse(
        response_text="I'm here to help you shop! Try asking about specific products like 'running shoes', 'electronics', or 'gifts'.",
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
        # Fallback if specific store has no sales in synthetic data
        # Use global data for demo purposes if store specific data is missing
        store_sales = transactions_df 
        # raise HTTPException(status_code=404, detail="No sales data for this store.")

    # Aggregate sales by day
    daily_sales = store_sales.set_index('timestamp').resample('D')['total_price'].sum().reset_index()
    daily_sales = daily_sales.rename(columns={'timestamp': 'ds', 'total_price': 'y'})

    if len(daily_sales) < 2:
         raise HTTPException(status_code=404, detail="Not enough data for forecast.")

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
    try:
        stockout_item = items_df[items_df['store_id'] == store_id].sample(1).iloc[0]['name']
    except:
        stockout_item = "N/A"

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

# --- NEW Analytics Endpoints ---

@router.get("/analytics/market-basket", response_model=List[MarketBasketRule])
async def get_market_basket_analysis():
    """
    Returns association rules (items frequently bought together).
    """
    if not analytics_engine:
        raise HTTPException(status_code=503, detail="Analytics engine not initialized")
    return analytics_engine.market_basket_analysis()

@router.get("/analytics/customer-segments", response_model=List[CustomerSegment])
async def get_customer_segments():
    """
    Returns customer segments based on clustering.
    """
    if not analytics_engine:
        raise HTTPException(status_code=503, detail="Analytics engine not initialized")
    
    segments = analytics_engine.customer_segmentation()
    # Map dictionary keys to match Pydantic model
    return [
        CustomerSegment(
            cluster=s['cluster'],
            segment_name=s['segment_name'],
            total_spend=s['total_spend'],
            avg_txn_value=s['avg_txn_value'],
            frequency=s['frequency'],
            customer_count=s['customer_id'] # Count was aggregated into this key
        ) for s in segments
    ]

@router.get("/customers/{customer_id}/insights", response_model=CustomerInsight)
async def get_customer_insights(customer_id: str):
    """
    Returns insights for a specific customer.
    """
    if not analytics_engine:
        raise HTTPException(status_code=503, detail="Analytics engine not initialized")
    
    insights = analytics_engine.get_customer_insights(customer_id)
    if not insights:
        raise HTTPException(status_code=404, detail="Customer not found")
    return insights

@router.get("/analytics/seasonal-analysis", response_model=List[SeasonalAnalysis])
async def get_seasonal_analysis():
    """
    Returns monthly sales trends.
    """
    if not analytics_engine:
        raise HTTPException(status_code=503, detail="Analytics engine not initialized")
    return analytics_engine.seasonal_analysis()

@router.get("/analytics/time-habits", response_model=TimeHabits)
async def get_time_habits():
    """
    Returns sales by day of week and hour of day.
    """
    if not analytics_engine:
        raise HTTPException(status_code=503, detail="Analytics engine not initialized")
    return analytics_engine.time_based_habits()

@router.get("/analytics/sentiment", response_model=List[SentimentAnalysis])
async def get_sentiment_analysis():
    """
    Returns sentiment analysis of reviews.
    """
    if not analytics_engine:
        raise HTTPException(status_code=503, detail="Analytics engine not initialized")
    return analytics_engine.sentiment_analysis()

@router.get("/analytics/persona-insights", response_model=List[PersonaAnalysis])
async def get_persona_insights():
    """
    Returns spending habits by customer persona.
    """
    if not analytics_engine:
        raise HTTPException(status_code=503, detail="Analytics engine not initialized")
    return analytics_engine.persona_analysis()
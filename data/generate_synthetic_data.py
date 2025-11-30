import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

print("Generating profound and insightful synthetic data...")

# --- 1. Enhanced Stores (20 Stores across categories) ---
stores_data = [
    # Fashion & Apparel
    {'store_id': 's1', 'name': 'Zara', 'category': 'Fashion', 'zone': 'A', 'tier': 'Premium'},
    {'store_id': 's2', 'name': 'H&M', 'category': 'Fashion', 'zone': 'A', 'tier': 'Mid-Range'},
    {'store_id': 's3', 'name': 'Gucci', 'category': 'Luxury', 'zone': 'B', 'tier': 'Luxury'},
    {'store_id': 's4', 'name': 'Nike', 'category': 'Sports', 'zone': 'A', 'tier': 'Mid-Range'},
    {'store_id': 's5', 'name': 'Uniqlo', 'category': 'Fashion', 'zone': 'A', 'tier': 'Budget'},
    # Electronics
    {'store_id': 's6', 'name': 'Apple Store', 'category': 'Electronics', 'zone': 'B', 'tier': 'Premium'},
    {'store_id': 's7', 'name': 'Samsung', 'category': 'Electronics', 'zone': 'B', 'tier': 'Mid-Range'},
    {'store_id': 's8', 'name': 'Croma', 'category': 'Electronics', 'zone': 'B', 'tier': 'Mid-Range'},
    # Food & Beverage
    {'store_id': 's9', 'name': 'Starbucks', 'category': 'Food', 'zone': 'C', 'tier': 'Mid-Range'},
    {'store_id': 's10', 'name': 'McDonalds', 'category': 'Food', 'zone': 'C', 'tier': 'Budget'},
    {'store_id': 's11', 'name': 'The Cheesecake Factory', 'category': 'Food', 'zone': 'C', 'tier': 'Premium'},
    {'store_id': 's12', 'name': 'Subway', 'category': 'Food', 'zone': 'C', 'tier': 'Budget'},
    # Entertainment & Leisure
    {'store_id': 's13', 'name': 'PVR Cinemas', 'category': 'Entertainment', 'zone': 'D', 'tier': 'Mid-Range'},
    {'store_id': 's14', 'name': 'Fun City', 'category': 'Entertainment', 'zone': 'D', 'tier': 'Mid-Range'},
    {'store_id': 's15', 'name': 'Crossword', 'category': 'Books', 'zone': 'D', 'tier': 'Mid-Range'},
    # Beauty & Health
    {'store_id': 's16', 'name': 'Sephora', 'category': 'Beauty', 'zone': 'A', 'tier': 'Premium'},
    {'store_id': 's17', 'name': 'MAC Cosmetics', 'category': 'Beauty', 'zone': 'A', 'tier': 'Premium'},
    {'store_id': 's18', 'name': 'The Body Shop', 'category': 'Beauty', 'zone': 'A', 'tier': 'Mid-Range'},
    # Home
    {'store_id': 's19', 'name': 'Home Centre', 'category': 'Home', 'zone': 'B', 'tier': 'Mid-Range'},
    {'store_id': 's20', 'name': 'IKEA Studio', 'category': 'Home', 'zone': 'B', 'tier': 'Budget'},
]
stores_df = pd.DataFrame(stores_data)
stores_df.to_csv('data/stores.csv', index=False)
print("-> stores.csv generated (20 stores).")

# --- 2. Detailed Products (Inventory) ---
items_data = []
item_id_counter = 1

# Helper to generate products based on category
def generate_products(store):
    products = []
    if store['category'] == 'Fashion':
        products = [
            ('Slim Fit Jeans', 2500), ('Cotton T-Shirt', 800), ('Summer Dress', 3500), 
            ('Leather Jacket', 8000), ('Formal Shirt', 2200), ('Sneakers', 4000)
        ]
    elif store['category'] == 'Luxury':
        products = [
            ('Leather Handbag', 150000), ('Designer Sunglasses', 35000), ('Silk Scarf', 25000),
            ('Premium Watch', 250000), ('Evening Gown', 120000)
        ]
    elif store['category'] == 'Electronics':
        products = [
            ('Smartphone', 60000), ('Laptop', 90000), ('Wireless Earbuds', 15000),
            ('Smartwatch', 25000), ('4K TV', 55000), ('Tablet', 40000)
        ]
    elif store['category'] == 'Food':
        products = [
            ('Cappuccino', 350), ('Burger Meal', 450), ('Pasta Alfredo', 650),
            ('Sandwich Combo', 300), ('Cheesecake Slice', 400), ('Pizza', 800)
        ]
    elif store['category'] == 'Entertainment':
        products = [
            ('Movie Ticket', 400), ('Popcorn Combo', 600), ('Bowling Game', 500),
            ('Arcade Card', 1000)
        ]
    elif store['category'] == 'Beauty':
        products = [
            ('Lipstick', 1800), ('Foundation', 3500), ('Perfume', 6000),
            ('Skincare Kit', 4500), ('Face Mask', 500)
        ]
    elif store['category'] == 'Books':
        products = [
            ('Bestseller Novel', 500), ('Business Book', 800), ('Cookbook', 1200),
            ('Stationery Set', 600), ('Magazine', 200)
        ]
    elif store['category'] == 'Home':
        products = [
            ('Cushion Cover', 800), ('Table Lamp', 2500), ('Bed Sheet Set', 3000),
            ('Scented Candle', 1200), ('Wall Clock', 1500)
        ]
    else: # Sports
        products = [
            ('Running Shoes', 5000), ('Yoga Mat', 1500), ('Dri-Fit Tee', 2000),
            ('Gym Bag', 3000), ('Training Shorts', 1800)
        ]
    
    return products

for _, store in stores_df.iterrows():
    products = generate_products(store)
    for name, price in products:
        # Add some price variation based on tier
        multiplier = 1.5 if store['tier'] == 'Premium' else (2.5 if store['tier'] == 'Luxury' else 1.0)
        final_price = int(price * multiplier)
        
        items_data.append({
            'item_id': f"i{item_id_counter}",
            'store_id': store['store_id'],
            'name': name,
            'category': store['category'],
            'price': final_price,
            'description': f"{store['tier']} quality {name} from {store['name']}."
        })
        item_id_counter += 1

items_df = pd.DataFrame(items_data)
items_df.to_csv('data/items.csv', index=False)
print(f"-> items.csv generated ({len(items_df)} items).")

# --- 3. Rich Customer Personas ---
customers_data = []
personas = ['Student', 'Professional', 'Parent', 'Tourist', 'Luxury Shopper']

for i in range(500):
    persona = random.choices(personas, weights=[0.3, 0.3, 0.2, 0.15, 0.05])[0]
    
    if persona == 'Student':
        age = random.randint(18, 24)
        income = random.randint(0, 300000)
        tier = 'Bronze'
    elif persona == 'Professional':
        age = random.randint(25, 45)
        income = random.randint(800000, 3000000)
        tier = random.choice(['Silver', 'Gold'])
    elif persona == 'Parent':
        age = random.randint(30, 55)
        income = random.randint(1000000, 4000000)
        tier = random.choice(['Silver', 'Gold'])
    elif persona == 'Tourist':
        age = random.randint(20, 60)
        income = random.randint(500000, 2000000)
        tier = 'Bronze' # One-time visitors usually
    else: # Luxury Shopper
        age = random.randint(30, 65)
        income = random.randint(5000000, 20000000)
        tier = 'Platinum'

    customers_data.append({
        'customer_id': f"c{i+1}",
        'name': f"Customer {i+1}",
        'age': age,
        'gender': random.choice(['Male', 'Female', 'Other']),
        'persona': persona,
        'annual_income': income,
        'membership_tier': tier
    })

customers_df = pd.DataFrame(customers_data)
customers_df.to_csv('data/customers.csv', index=False)
print("-> customers.csv generated (500 profiles).")

# --- 4. Complex Transactions (Shopping Trips) ---
transactions_data = []
reviews_data = []
start_date = datetime.now() - timedelta(days=180) # 6 months data

# Define persona preferences (Store Categories)
preferences = {
    'Student': ['Food', 'Entertainment', 'Fashion', 'Books'],
    'Professional': ['Electronics', 'Fashion', 'Food', 'Home'],
    'Parent': ['Home', 'Food', 'Fashion', 'Beauty'],
    'Tourist': ['Fashion', 'Food', 'Luxury', 'Entertainment'],
    'Luxury Shopper': ['Luxury', 'Beauty', 'Electronics', 'Premium Food']
}

txn_counter = 1
review_counter = 1

for _ in range(3000): # 3000 trips
    # Pick a random day
    trip_date = start_date + timedelta(days=random.randint(0, 179))
    
    # Weekend multiplier (more trips on weekends)
    if trip_date.weekday() >= 5: 
        if random.random() > 0.3: continue # Skip some weekends to balance, but generally busier
    
    # Pick a customer
    customer = customers_df.sample(1).iloc[0]
    persona_prefs = preferences[customer['persona']]
    
    # Determine number of stores visited in this trip
    num_stores = random.randint(1, 4)
    
    # Filter stores matching persona preferences
    preferred_stores = stores_df[stores_df['category'].isin(persona_prefs)]
    if preferred_stores.empty:
        preferred_stores = stores_df # Fallback
        
    visited_stores = preferred_stores.sample(min(num_stores, len(preferred_stores)))
    
    for _, store in visited_stores.iterrows():
        # Buy items from this store
        store_items = items_df[items_df['store_id'] == store['store_id']]
        if store_items.empty: continue
        
        num_items = random.randint(1, 3)
        items_bought = store_items.sample(num_items)
        
        item_ids = items_bought['item_id'].tolist()
        total_price = items_bought['price'].sum()
        
        # Add Transaction
        transactions_data.append({
            'txn_id': f"t{txn_counter}",
            'store_id': store['store_id'],
            'customer_id': customer['customer_id'],
            'items': ",".join(item_ids),
            'total_price': total_price,
            'timestamp': trip_date.replace(hour=random.randint(10, 21), minute=random.randint(0, 59)).isoformat()
        })
        txn_counter += 1
        
        # 20% chance to leave a review
        if random.random() < 0.2:
            sentiment_score = random.choice([1, 2, 3, 4, 5])
            # Generate dummy review text based on score
            if sentiment_score >= 4:
                text = random.choice(["Loved it!", "Great service.", "Amazing quality.", "Will come again.", "Best purchase ever!"])
            elif sentiment_score == 3:
                text = random.choice(["It was okay.", "Average experience.", "Decent but pricey.", "Not bad."])
            else:
                text = random.choice(["Terrible service.", "Too expensive.", "Quality is poor.", "Disappointed.", "Never coming back."])
                
            reviews_data.append({
                'review_id': f"r{review_counter}",
                'store_id': store['store_id'],
                'customer_id': customer['customer_id'],
                'rating': sentiment_score,
                'text': text,
                'timestamp': trip_date.isoformat()
            })
            review_counter += 1

transactions_df = pd.DataFrame(transactions_data)
transactions_df.to_csv('data/transactions.csv', index=False)

reviews_df = pd.DataFrame(reviews_data)
reviews_df.to_csv('data/reviews.csv', index=False)

print(f"-> transactions.csv generated ({len(transactions_df)} records).")
print(f"-> reviews.csv generated ({len(reviews_df)} records).")
print("Data generation complete. Profound insights await!")
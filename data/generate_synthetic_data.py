import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

print("Generating synthetic data...")

# 1. Stores
stores_data = {
    'store_id': [f"s{i+1}" for i in range(5)],
    'name': ['Apex Sports', 'Fashion Forward', 'TechTrove', 'Gourmet Corner', 'Book Nook'],
    'mall_zone': ['A', 'B', 'C', 'A', 'B'],
    'store_type': ['Sports', 'Apparel', 'Electronics', 'Food', 'Books']
}
stores_df = pd.DataFrame(stores_data)
stores_df.to_csv('data/stores.csv', index=False)
print("-> stores.csv generated.")

# 2. Items
items_data = []
item_categories = {
    'Apex Sports': [('Running Shoes', 4500), ('Yoga Mat', 1500), ('Dumbbells', 3000)],
    'Fashion Forward': [('Denim Jeans', 2500), ('Summer Dress', 3200), ('Leather Jacket', 7000)],
    'TechTrove': [('Wireless Earbuds', 5000), ('Smartwatch', 12000), ('Power Bank', 2000)],
    'Gourmet Corner': [('Artisan Cheese', 800), ('Imported Olives', 500), ('Dark Chocolate', 600)],
    'Book Nook': [('Sci-Fi Novel', 700), ('Cookbook', 1100), ('Mystery Thriller', 650)]
}

item_id_counter = 1
for i, store in stores_df.iterrows():
    store_name = store['name']
    store_id = store['store_id']
    for item_name, price in item_categories[store_name]:
        items_data.append({
            'item_id': f"i{item_id_counter}",
            'store_id': store_id,
            'name': item_name,
            'category': store['store_type'],
            'price': price,
            'description': f"A high-quality {item_name} from {store_name}."
        })
        item_id_counter += 1

items_df = pd.DataFrame(items_data)
items_df.to_csv('data/items.csv', index=False)
print("-> items.csv generated.")

# 3. Transactions (Sales)
transactions_data = []
start_date = datetime.now() - timedelta(days=90)
for i in range(1000):
    date = start_date + timedelta(days=random.randint(0, 89), hours=random.randint(9, 20))
    # ਲਾਈਨ 53 (ਠੀਕ ਕੀਤੀ ਹੋਈ)
    store_id = random.choice(stores_df['store_id'].tolist())
    store_items = items_df[items_df['store_id'] == store_id]
    
    num_items_in_txn = random.randint(1, 3)
    items_bought = []
    total_price = 0
    
    for _ in range(num_items_in_txn):
        item = store_items.sample(1).iloc[0]
        items_bought.append(item['item_id'])
        total_price += item['price']
        
    transactions_data.append({
        'txn_id': f"t{i+1}",
        'store_id': store_id,
        'items': ",".join(items_bought), # Simple CSV for items
        'total_price': total_price,
        'timestamp': date.isoformat()
    })

transactions_df = pd.DataFrame(transactions_data)
transactions_df.to_csv('data/transactions.csv', index=False)
print("-> transactions.csv generated.")
print("Data generation complete.")
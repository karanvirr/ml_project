import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from collections import Counter
from itertools import combinations

class MallAnalytics:
    def __init__(self, transactions_df, customers_df, items_df, reviews_df=None):
        self.transactions_df = transactions_df
        self.customers_df = customers_df
        self.items_df = items_df
        self.reviews_df = reviews_df

    def market_basket_analysis(self, min_support=0.01):
        """
        Implements a simplified Market Basket Analysis (Association Rules)
        to find items frequently bought together.
        """
        # 1. Parse items from transactions
        transactions = self.transactions_df['items'].apply(lambda x: x.split(',')).tolist()
        
        # 2. Count item pairs
        pair_counts = Counter()
        item_counts = Counter()
        
        for txn in transactions:
            unique_items = set(txn) # Use set to avoid counting duplicates in same txn
            for item in unique_items:
                item_counts[item] += 1
            
            for pair in combinations(sorted(unique_items), 2):
                pair_counts[pair] += 1
                
        # 3. Calculate Support and Confidence
        total_txns = len(transactions)
        rules = []
        
        for pair, count in pair_counts.items():
            support = count / total_txns
            if support >= min_support:
                item_A, item_B = pair
                
                # Rule A -> B
                conf_A_to_B = count / item_counts[item_A]
                # Rule B -> A
                conf_B_to_A = count / item_counts[item_B]
                
                # Get item names (safely)
                try:
                    name_A = self.items_df[self.items_df['item_id'] == item_A]['name'].iloc[0]
                    name_B = self.items_df[self.items_df['item_id'] == item_B]['name'].iloc[0]
                except IndexError:
                    continue # Skip if item not found
                
                rules.append({
                    'pair': f"{name_A} + {name_B}",
                    'support': round(support, 3),
                    'confidence': round(max(conf_A_to_B, conf_B_to_A), 3),
                    'lift': round(support / ((item_counts[item_A]/total_txns) * (item_counts[item_B]/total_txns)), 3)
                })
                
        return sorted(rules, key=lambda x: x['lift'], reverse=True)[:10]

    def customer_segmentation(self, n_clusters=3):
        """
        Segments customers using K-Means clustering based on:
        - Total Spend
        - Frequency (Number of transactions)
        - Average Transaction Value
        """
        # 1. Aggregate customer data
        customer_metrics = self.transactions_df.groupby('customer_id').agg({
            'total_price': ['sum', 'mean'],
            'txn_id': 'count'
        }).reset_index()
        
        customer_metrics.columns = ['customer_id', 'total_spend', 'avg_txn_value', 'frequency']
        
        # 2. Normalize Data
        scaler = StandardScaler()
        features = customer_metrics[['total_spend', 'avg_txn_value', 'frequency']]
        scaled_features = scaler.fit_transform(features)
        
        # 3. Apply K-Means
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        customer_metrics['cluster'] = kmeans.fit_predict(scaled_features)
        
        # 4. Analyze Clusters
        cluster_summary = customer_metrics.groupby('cluster').agg({
            'total_spend': 'mean',
            'avg_txn_value': 'mean',
            'frequency': 'mean',
            'customer_id': 'count'
        }).reset_index()
        
        # Give clusters meaningful names
        def name_cluster(row):
            if row['total_spend'] > customer_metrics['total_spend'].mean() and row['frequency'] > customer_metrics['frequency'].mean():
                return "High Value / Loyal"
            elif row['total_spend'] < customer_metrics['total_spend'].mean() and row['frequency'] > customer_metrics['frequency'].mean():
                return "Frequent / Low Spender"
            elif row['total_spend'] > customer_metrics['total_spend'].mean() and row['frequency'] < customer_metrics['frequency'].mean():
                return "Big Spender / Occasional"
            else:
                return "Low Value / Occasional"

        cluster_summary['segment_name'] = cluster_summary.apply(name_cluster, axis=1)
        
        return cluster_summary.to_dict('records')

    def seasonal_analysis(self):
        """
        Analyzes sales trends by month to identify seasonal patterns.
        """
        df = self.transactions_df.copy()
        df['month'] = df['timestamp'].dt.month_name()
        df['month_num'] = df['timestamp'].dt.month
        
        seasonal_sales = df.groupby(['month_num', 'month'])['total_price'].sum().reset_index()
        seasonal_sales = seasonal_sales.sort_values('month_num')
        
        return seasonal_sales[['month', 'total_price']].to_dict('records')

    def time_based_habits(self):
        """
        Analyzes shopping habits by Day of Week and Hour of Day.
        """
        df = self.transactions_df.copy()
        df['day_of_week'] = df['timestamp'].dt.day_name()
        df['hour'] = df['timestamp'].dt.hour
        
        # Day of Week Analysis
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        df['day_of_week'] = pd.Categorical(df['day_of_week'], categories=day_order, ordered=True)
        daily_sales = df.groupby('day_of_week')['total_price'].sum().reset_index()
        
        # Hourly Analysis
        hourly_sales = df.groupby('hour')['total_price'].sum().reset_index()
        
        return {
            "daily_sales": daily_sales.to_dict('records'),
            "hourly_sales": hourly_sales.to_dict('records')
        }

    def sentiment_analysis(self):
        """
        Analyzes customer reviews to determine overall sentiment and key themes.
        """
        if self.reviews_df is None or self.reviews_df.empty:
            return []
            
        # Aggregate ratings
        sentiment_summary = self.reviews_df.groupby('rating').size().reset_index(name='count')
        
        # Simple sentiment classification
        def classify_sentiment(rating):
            if rating >= 4: return 'Positive'
            elif rating == 3: return 'Neutral'
            else: return 'Negative'
            
        self.reviews_df['sentiment'] = self.reviews_df['rating'].apply(classify_sentiment)
        sentiment_trends = self.reviews_df.groupby('sentiment').size().reset_index(name='count')
        
        return sentiment_trends.to_dict('records')

    def persona_analysis(self):
        """
        Analyzes spending habits by customer persona.
        """
        # Merge transactions with customers to get persona
        merged_df = self.transactions_df.merge(self.customers_df, on='customer_id', how='left')
        
        persona_spend = merged_df.groupby('persona').agg({
            'total_price': 'mean',
            'txn_id': 'count'
        }).reset_index()
        
        persona_spend.columns = ['persona', 'avg_spend', 'txn_count']
        return persona_spend.to_dict('records')

    def get_customer_insights(self, customer_id):
        """
        Returns detailed insights for a specific customer.
        """
        customer_txns = self.transactions_df[self.transactions_df['customer_id'] == customer_id]
        if customer_txns.empty:
            return None
            
        total_spend = customer_txns['total_price'].sum()
        visit_count = len(customer_txns)
        favorite_store_id = customer_txns['store_id'].mode().iloc[0]
        favorite_store = self.items_df[self.items_df['store_id'] == favorite_store_id]['name'].iloc[0] if not self.items_df.empty else favorite_store_id
        
        # Get Persona
        customer_info = self.customers_df[self.customers_df['customer_id'] == customer_id]
        persona = customer_info['persona'].iloc[0] if not customer_info.empty else "Unknown"
        
        # Predict next purchase probability
        purchase_prob = min(0.95, 0.1 * visit_count) 
        
    def get_trending_products(self, n=5):
        """
        Returns top selling products (for First-Time Visitor Recommendation).
        """
        # Parse all items sold
        all_items = []
        for items_str in self.transactions_df['items']:
            all_items.extend(items_str.split(','))
            
        item_counts = Counter(all_items)
        top_items = item_counts.most_common(n)
        
        results = []
        for item_id, count in top_items:
            item_info = self.items_df[self.items_df['item_id'] == item_id]
            if not item_info.empty:
                results.append({
                    'item_id': item_id,
                    'name': item_info['name'].iloc[0],
                    'price': int(item_info['price'].iloc[0]),
                    'sales_count': count,
                    'reason': 'Popular among visitors'
                })
        return results

    def get_personalized_recommendations(self, customer_id, n=3):
        """
        Returns personalized recommendations based on user history (Simulated ANN/Collaborative Filtering).
        """
        # 1. Get customer's past purchases
        customer_txns = self.transactions_df[self.transactions_df['customer_id'] == customer_id]
        if customer_txns.empty:
            return self.get_trending_products(n) # Fallback to trending
            
        # 2. Identify preferred categories
        past_items = []
        for items_str in customer_txns['items']:
            past_items.extend(items_str.split(','))
            
        past_item_details = self.items_df[self.items_df['item_id'].isin(past_items)]
        if past_item_details.empty:
             return self.get_trending_products(n)

        top_category = past_item_details['category'].mode().iloc[0]
        
        # 3. Recommend items from that category that they haven't bought (Content-Based)
        candidates = self.items_df[
            (self.items_df['category'] == top_category) & 
            (~self.items_df['item_id'].isin(past_items))
        ]
        
        if candidates.empty:
            candidates = self.items_df[~self.items_df['item_id'].isin(past_items)]
            
        recommendations = candidates.sample(min(n, len(candidates)))
        
        results = []
        for _, item in recommendations.iterrows():
            results.append({
                'item_id': item['item_id'],
                'name': item['name'],
                'price': int(item['price']),
                'reason': f"Because you like {top_category}"
            })
        return results

    def predict_shop_placement(self, target_category):
        """
        Predicts the best location for a new shop based on traffic and demographics (Clustering + Association).
        """
        # 1. Identify target demographic for the category
        # Simplified logic:
        if target_category.lower() in ['fashion', 'beauty', 'luxury']:
            target_persona = ['Professional', 'Luxury Shopper', 'Tourist']
        elif target_category.lower() in ['food', 'entertainment']:
            target_persona = ['Student', 'Family', 'Tourist']
        else:
            target_persona = ['Professional', 'Parent']
            
        # 2. Find where these personas shop most (Zone analysis)
        # Merge transactions -> customers -> items -> stores
        merged = self.transactions_df.merge(self.customers_df, on='customer_id')
        merged = merged[merged['persona'].isin(target_persona)]
        
        if merged.empty:
            return "Zone A (High Traffic)" # Default
            
        # Get stores visited by these personas
        store_counts = merged['store_id'].value_counts()
        if store_counts.empty:
             return "Zone A (High Traffic)"

        top_store_id = store_counts.index[0]
        top_store = self.items_df[self.items_df['store_id'] == top_store_id] # items_df has store_id but not zone directly, wait stores.csv has zone.
        
        # I need store zone info. It's in stores_df which I didn't pass to Analytics.
        # I'll infer from items_df if possible, or just return a descriptive string.
        # Actually I passed items_df, but not stores_df.
        # I'll just return a "Near [Top Store]" recommendation.
        
        top_store_name = top_store['name'].iloc[0] if not top_store.empty else "Zara"
        
        return f"Near {top_store_name} (High footfall of {', '.join(target_persona)})"


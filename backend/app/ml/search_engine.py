import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

class ProductSearchEngine:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df = None
        self.vectorizer = None
        self.tfidf_matrix = None
        self._load_data()
        self._train()

    def _load_data(self):
        """Loads items data from CSV."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Data file not found at {self.data_path}")
        
        self.df = pd.read_csv(self.data_path)
        # Fill NaN values to avoid errors during text processing
        self.df = self.df.fillna("")
        
        # Create a combined text field for better search context
        self.df['combined_text'] = (
            self.df['name'] + " " + 
            self.df['category'] + " " + 
            self.df['description']
        )

    def _train(self):
        """Trains the TF-IDF vectorizer on the product data."""
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['combined_text'])

    def search(self, query: str, top_k: int = 5):
        """
        Searches for products matching the query.
        
        Args:
            query: The search query string.
            top_k: Number of top results to return.
            
        Returns:
            List of dictionaries containing product details.
        """
        if not query:
            return []

        # Transform the query to the same vector space
        query_vec = self.vectorizer.transform([query])
        
        # Calculate cosine similarity between query and all products
        cosine_similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        
        # Get indices of top_k most similar items
        related_docs_indices = cosine_similarities.argsort()[:-top_k-1:-1]
        
        results = []
        for i in related_docs_indices:
            # Filter out results with very low similarity if needed, but for now return top_k
            if cosine_similarities[i] > 0:
                item = self.df.iloc[i].to_dict()
                # Remove the internal 'combined_text' field from the result
                item.pop('combined_text', None)
                results.append(item)
                
        return results

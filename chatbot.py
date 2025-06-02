import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

class NLPChatbot:
    def __init__(self):
        # Questions and answers
        self.qa_pairs = [
            {"question": "What are your opening hours?", 
             "answer": "We're open Monday to Friday, 9 AM to 5 PM."},
            {"question": "How can I contact support?", 
             "answer": "Email us at support@company.com or call (555) 123-4567."},
            {"question": "Do you offer refunds?", 
             "answer": "Yes, we offer 30-day refunds for unused products."},
            {"question": "Where is your company located?", 
             "answer": "Our headquarters is at 123 Main St, Anytown, USA."}
        ]
        
        # Prepare TF-IDF vectors
        self.questions = [pair["question"] for pair in self.qa_pairs]
        self.vectorizer = TfidfVectorizer()
        self.question_vectors = self.vectorizer.fit_transform(self.questions)
    
    def respond(self, user_input):
        # Vectorize user input
        input_vector = self.vectorizer.transform([user_input])
        
        # Calculate similarity with stored questions
        similarities = cosine_similarity(input_vector, self.question_vectors)
        best_match_idx = np.argmax(similarities)
        
        # Threshold for considering a match (adjust as needed)
        if similarities[0, best_match_idx] > 0.5:
            return self.qa_pairs[best_match_idx]["answer"]
        else:
            return "I'm not sure I understand. Could you provide more details?"

# Usage
bot = NLPChatbot()
print(bot.respond(input("What is your concern today?")))

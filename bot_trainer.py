import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

class NLPChatbotTrainer:
    def __init__(self):
        self.qa_pairs = [
            {"question": "What are your opening hours?", 
             "answer": "We're open Monday to Friday, 9 AM to 5 PM."},
            {"question": "How can I contact support?", 
             "answer": "Email us at support@company.com or call (555) 123-4567."},
            {"question": "Do you offer refunds?", 
             "answer": "Yes, we offer 30-day refunds for unused products."},
            {"question": "Where is your company located?", 
             "answer": "Our headquarters is at 123 Main St, Anytown, USA."},
            {"question": "What are your major products?", 
             "answer": "We provide Large Language Model (LLM) based services."},
            {"question": "How long do you require to deliver the product?", 
             "answer": "We deliver our products within a week."},
            {"question": "What are the forms of payment?", 
             "answer": "You can use either Debit/Credit Card, Bank Account, or pay cash when you are in-person at our office outlet."}
        ]
        
        self.questions = [pair["question"] for pair in self.qa_pairs]
        self.vectorizer = TfidfVectorizer()
        self.question_vectors = self.vectorizer.fit_transform(self.questions)
    
    def save_model(self, file_path):
        """Save the trained model to a file"""
        with open(file_path, 'wb') as f:
            pickle.dump({
                'qa_pairs': self.qa_pairs,
                'questions': self.questions,
                'vectorizer': self.vectorizer,
                'question_vectors': self.question_vectors
            }, f)
        print(f"Model successfully saved to {file_path}")

if __name__ == "__main__":
    # Train and save the model
    trainer = NLPChatbotTrainer()
    trainer.save_model('chatbot_model.pkl')

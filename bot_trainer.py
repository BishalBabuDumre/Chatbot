import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import json

with open("qa_pairs.json", "r") as f:
    data = json.load(f)

class NLPChatbotTrainer:
    def __init__(self):
        self.qa_pairs = data["qa_pairs"]        
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

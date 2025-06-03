import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle

class NLPChatbot:
    def __init__(self, model_path):
        # Load the pre-trained model
        with open(model_path, 'rb') as f:
            data = pickle.load(f)
            self.qa_pairs = data['qa_pairs']
            self.questions = data['questions']
            self.vectorizer = data['vectorizer']
            self.question_vectors = data['question_vectors']
    
    def respond(self, user_input):
        # Vectorize user input
        input_vector = self.vectorizer.transform([user_input])
        
        # Calculate similarity with stored questions
        similarities = cosine_similarity(input_vector, self.question_vectors)
        best_match_idx = np.argmax(similarities)
        
        # Threshold for considering a match
        if similarities[0, best_match_idx] > 0.5:
            return self.qa_pairs[best_match_idx]["answer"]
        else:
            return "I'm not sure I understand. Could you provide more details?"

if __name__ == "__main__":
    # Load and use the model
    bot = NLPChatbot('chatbot_model.pkl')
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Chatbot: Goodbye!")
            break
        response = bot.respond(user_input)
        print("Chatbot:", response)
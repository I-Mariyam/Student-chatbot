import pandas as pd
import random

class StudentChatbot:
    def __init__(self, faq_file="data/faqs.csv"):
        # Load FAQ dataset
        try:
            self.faqs = pd.read_csv(faq_file)
        except FileNotFoundError:
            print("⚠️ FAQ file not found. Make sure 'data/faqs.csv' exists.")
            self.faqs = pd.DataFrame(columns=["question", "answer"])

    def get_response(self, user_input):
        user_input = user_input.lower()

        # Search for partial matches
for i, row in self.faqs.iterrows():
    question = row["question"].lower()
    if any(word in user_input for word in question.split()):
        return row["answer"]


        # If no exact match, return fallback
        fallback_responses = [
            "I'm not sure about that. Can you ask in another way?",
            "Sorry, I don’t know this yet. You can check with the admin office.",
            "Hmm, I couldn’t find an answer. Maybe try rephrasing your question?"
        ]
        return random.choice(fallback_responses)


# Run chatbot in terminal
if __name__ == "__main__":
    bot = StudentChatbot()

    print("👩‍💻 Student Chatbot (type 'exit' to quit)\n")
    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit"]:
            print("Chatbot: Goodbye! 👋")
            break
        response = bot.get_response(query)
        print("Chatbot:", response)

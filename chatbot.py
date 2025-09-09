import pandas as pd

class Chatbot:
    def __init__(self, faq_file):
        self.faqs = pd.read_csv(faq_file)

    def get_response(self, user_input):
        user_input = user_input.lower()
        
        # Search for matches
        for i, row in self.faqs.iterrows():
            if row["question"].lower() in user_input:
                return row["answer"]
        
        return "I'm not sure about that. Can you ask in another way?"

if __name__ == "__main__":
    bot = Chatbot("data/faqs.csv")
    print("👩‍💻 Student Chatbot (type 'exit' to quit)\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Chatbot: Goodbye!")
            break
        response = bot.get_response(user_input)
        print("Chatbot:", response)

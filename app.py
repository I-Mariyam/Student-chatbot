# app.py
from flask import Flask, request, jsonify, render_template
from chatbot import FAQChatbot

app = Flask(__name__, static_folder='static', template_folder='templates')
bot = FAQChatbot()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    message = data.get('message', '')
    answer, confidence = bot.get_response(message)
    if answer:
        return jsonify({'answer': answer, 'confidence': confidence})
    else:
        fallback = ("Sorry, I don't have an answer for that yet. "
                    "You can try rephrasing, check the student portal, or contact the registrar.")
        return jsonify({'answer': fallback, 'confidence': confidence})

if __name__ == '__main__':
    app.run(debug=True)

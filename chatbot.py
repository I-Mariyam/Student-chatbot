# chatbot.py
import pandas as pd
import numpy as np
import re
import os
import csv
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def preprocess(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

class FAQChatbot:
    def __init__(self, faq_path='data/faqs.csv', unknowns_path='data/unknowns.csv', threshold=0.35):
        self.faq_path = faq_path
        self.unknowns_path = unknowns_path
        self.threshold = threshold
        self._load_faqs()

    def _load_faqs(self):
        if not os.path.exists(self.faq_path):
            raise FileNotFoundError(f"{self.faq_path} not found. Please create it.")
        self.df = pd.read_csv(self.faq_path)
        if 'question' not in self.df.columns or 'answer' not in self.df.columns:
            raise ValueError("faqs.csv must have 'question' and 'answer' columns.")
        self.corpus = [preprocess(q) for q in self.df['question'].astype(str).tolist()]
        self.vectorizer = TfidfVectorizer(ngram_range=(1,2), stop_words='english')
        self.tfidf = self.vectorizer.fit_transform(self.corpus)

    def get_response(self, message: str):
        message_clean = preprocess(message)
        if not message_clean:
            return "Please type a question.", 0.0
        q_vec = self.vectorizer.transform([message_clean])
        sims = cosine_similarity(q_vec, self.tfidf)[0]
        idx = int(np.argmax(sims))
        score = float(sims[idx])
        if score >= self.threshold:
            answer = self.df.loc[idx, 'answer']
            return answer, score
        else:
            self._log_unknown(message, score)
            return None, score

    def _log_unknown(self, message, score):
        os.makedirs(os.path.dirname(self.unknowns_path), exist_ok=True)
        with open(self.unknowns_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().isoformat(), score, message])

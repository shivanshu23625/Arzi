import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from config.settings import get_settings
from common.schemas import SpamResult

settings = get_settings()

class SpamClassifierService:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
        self.model = LogisticRegression(C=5.0, max_iter=200) # Adjusted C value for slightly larger dataset
        self.is_trained = False
        self._bootstrap_default_model()

    def _bootstrap_default_model(self):
        # Expanded dataset for better accuracy
        synthetic_corpus = [
            "BUY CHEAP PHARMA ONLINE NOW FREE DISCOUNT",
            "CLAIM YOUR FREE MONEY WINNER",
            "CONGRATULATIONS you have WON a FREE PRIZE click now",
            "Get rich quick click here to claim your bitcoin",
            "Hot singles in your area want to meet you",
            "Can you provide a summary of project status?",
            "The streetlights in Ward 7 have been broken for three weeks.",
            "My ration card application is delayed, please provide the status.",
            "Requesting municipal tender records for the new highway project.",
            "I need assistance with my scholarship disbursement timeline.",
        ]
        synthetic_labels = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
        X = self.vectorizer.fit_transform(synthetic_corpus)
        self.model.fit(X, synthetic_labels)
        self.is_trained = True

    def predict(self, text: str) -> SpamResult:
        if not self.is_trained: raise RuntimeError("Model uninitialized.")
        features = self.vectorizer.transform([text])
        spam_prob = float(self.model.predict_proba(features)[0][1])
        return SpamResult(
            classification="SPAM" if spam_prob >= settings.SPAM_THRESHOLD else "AUTHENTIC",
            spam_score=spam_prob,
            authenticity_score=1 - spam_prob,
            reason=f"Probability: {spam_prob:.4f}"
        )
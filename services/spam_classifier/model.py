import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from config.settings import get_settings
from common.schemas import SpamResult

settings = get_settings()

class SpamClassifierService:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
        # C=1.0 over-regularized this tiny bootstrap set: even the exact spam
        # phrase "CLAIM YOUR FREE MONEY WINNER" only scored ~0.60, below most
        # policy thresholds. C=10.0 gives a sharper, more decisive boundary.
        self.model = LogisticRegression(C=10.0, max_iter=200)
        self.is_trained = False
        self._bootstrap_default_model()

    def _bootstrap_default_model(self):
        synthetic_corpus = [
            "BUY CHEAP PHARMA ONLINE NOW FREE DISCOUNT",
            "CLAIM YOUR FREE MONEY WINNER",
            "URGENT: Verify bank account password immediately",
            "CONGRATULATIONS you have WON a FREE PRIZE click now",
            "Limited time offer act now claim your reward",
            "Hello, please review the document for our meeting",
            "Can you provide a summary of project status?",
            "The user request requires database query assistance.",
            "Please schedule a call for next week to discuss the roadmap",
            "Attached is the report you asked for, let me know your thoughts",
        ]
        synthetic_labels = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
        X = self.vectorizer.fit_transform(synthetic_corpus)
        self.model.fit(X, synthetic_labels)
        self.is_trained = True

    def predict(self, text: str) -> SpamResult:
        if not self.is_trained:
            raise RuntimeError("Spam classification model state is uninitialized.")

        features = self.vectorizer.transform([text])
        probabilities = self.model.predict_proba(features)[0]
        spam_prob = float(probabilities[1])
        auth_prob = float(probabilities[0])

        is_spam = spam_prob >= settings.SPAM_THRESHOLD

        return SpamResult(
            classification="SPAM" if is_spam else "AUTHENTIC",
            spam_score=spam_prob,
            authenticity_score=auth_prob,
            reason=f"Classification determined with spam probability of {spam_prob:.4f}"
        )
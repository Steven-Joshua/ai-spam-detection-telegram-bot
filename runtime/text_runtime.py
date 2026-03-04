import joblib
import re

loaded_model = joblib.load("model/spam_classifier_model.pkl")
loaded_vectorizer = joblib.load("model/tfidf_vectorizer.pkl")

optimal_threshold = 0.24

def clean_text(text: str):
    text = re.sub(r"[^a-zA-Z0-9\s:/]", "", text.replace("\n", " ").strip())
    text = re.sub(r"\b[a-zA-Z]{1,2}\b", "", text)
    return text.lower()

def detect_spam_from_text(text: str):

    cleaned = clean_text(text)

    if not cleaned.strip():
        return {
            "status": "error",
            "message": "Invalid or empty text."
        }

    text_tfidf = loaded_vectorizer.transform([cleaned])
    spam_probability = loaded_model.predict_proba(text_tfidf)[:, 1][0]

    prediction = "Spam" if spam_probability > optimal_threshold else "Ham"

    return {
        "status": "success",
        "prediction": prediction,
        "spam_probability": round(float(spam_probability), 2),
        "text_preview": text[:200]
    }
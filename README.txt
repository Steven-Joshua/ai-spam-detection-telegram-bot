# 🤖 AI-Powered Spam Detection System

### (Machine Learning + LLM + FastAPI + Telegram Bot)

An end-to-end AI system that detects spam messages using a trained Machine Learning model and enhances predictions with LLM-based explanations. The system is deployed using FastAPI and integrated with a Telegram Bot for real-time interaction.

---

## 🚀 Project Overview

This project demonstrates:

* 📊 Machine Learning model development
* 🧠 LLM-based explanation layer
* 🌐 FastAPI backend deployment
* 📩 Telegram Bot integration
* 🖼 OCR-based image spam detection

It showcases both **Data Science modeling** and **AI/ML system deployment skills**.

---

## 🔬 Model Development (Data Science)

The spam classifier was built using:

* TF-IDF Vectorization
* Logistic Regression
* Train/Test Split
* Precision, Recall, F1-score
* Confusion Matrix analysis

Dataset:

```
dataset/mail_data_ml.csv
```

Model artifacts:

```
model/spam_classifier_model.pkl
model/tfidf_vectorizer.pkl
```

Training scripts:

```
training/Spam_engine.py
training/count.py
```

---

## 🏗 System Architecture

User → Telegram Bot → FastAPI → ML Model → LLM Explanation → Response

### Components:

* **ML Model** for spam classification
* **Confidence-aware predictions**
* **LLM integration (Groq API)** for explanation
* **OCR pipeline** for detecting spam in images
* **Modular runtime system**

---

## 📂 Project Structure

```
AI-SPAM-DETECTION-TELEGRAM/
│
├── app.py
├── agent.py
├── spam_tool.py
├── telegram_bot.py
│
├── dataset/
│   └── mail_data_ml.csv
│
├── model/
│   ├── spam_classifier_model.pkl
│   └── tfidf_vectorizer.pkl
│
├── training/
│   ├── Spam_engine.py
│   ├── Scrap_text_from_image.py
│   └── count.py
│
├── runtime/
│   ├── image_runtime.py
│   └── text_runtime.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🛠 Tech Stack

* FastAPI
* Uvicorn
* Scikit-learn
* Pandas / NumPy
* LangChain
* Groq (LLM inference)
* Python Telegram Bot
* OpenCV
* Tesseract OCR

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```
git clone <your_repo_url>
cd AI-SPAM-DETECTION-TELEGRAM
```

---

### 2️⃣ Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

### 4️⃣ Create Environment Variables

Create a `.env` file in the root folder:

```
GROQ_API_KEY=your_api_key_here
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

⚠️ Do NOT upload `.env` to GitHub.

---

## ▶️ Running the Application

Start FastAPI server:

```
uvicorn app:app --reload
```

Run Telegram bot:

```
python telegram_bot.py
```

---

## 🖼 OCR Requirement

If using image-based spam detection, install Tesseract OCR separately:

https://github.com/tesseract-ocr/tesseract

---

## 🎯 Key Features

* Hybrid ML + LLM architecture
* Real-time spam detection
* Image-based spam detection (OCR)
* Deployable API backend
* Modular project structure
* Production-ready folder organization

---

## 📌 Future Improvements

* Compare models (Naive Bayes, XGBoost)
* Docker containerization
* Cloud deployment (AWS/GCP)
* Add logging & monitoring
* CI/CD pipeline

---

## 👨‍💻 Author

Steven Joshua
MSc Data Science
AI/ML Engineer | Data Science

---

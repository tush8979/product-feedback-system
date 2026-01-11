# 🛒 Product Feedback Intelligent System

A **public, social-style product feedback platform** built with **Streamlit + Machine Learning**.  
Anyone can post feedback (text or audio), interact with posts, and explore trending products.

---

## 🚀 Live Features

- ✍️ Public product feedback (no login)
- 🎤 Audio → Text feedback (Whisper)
- 😊 ML-based sentiment analysis
- 👍 Unlimited likes / 👎 dislikes
- 💬 Comment system
- 🔥 Trending products
- 🔎 AI-powered semantic search
- 📱 Automatic product emojis
- 🎨 Social-media style UI (cards + feed)

---

## 🧠 Tech Stack

| Layer | Technology |
|-----|-----------|
Frontend | Streamlit + HTML/CSS |
ML / NLP | HuggingFace Transformers |
Audio | OpenAI Whisper |
Search | Sentence Transformers |
Storage | CSV (lightweight backend) |

---

## 📁 Project Structure
Product Feedback System/
├── app.py
├── requirements.txt
├── data/
│   ├── posts.csv
│   └── comments.csv
├── src/
│   ├── asr.py
│   ├── sentiment.py
│   └── semantic.py

---

## ▶️ Run Locally

```bash
# clone repo
git clone https://github.com/<your-username>/product-feedback-system.git
cd product-feedback-system

# create environment
python3 -m venv .venv
source .venv/bin/activate

# install dependencies
pip install -r requirements.txt

# install ffmpeg (macOS)
brew install ffmpeg

# run app
python -m streamlit run app.py

## 🚀 Live Demo

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://appuct-feedback-system-sl9ayrdplrw7pg3yrvxqcn.streamlit.app/)
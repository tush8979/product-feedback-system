from transformers import pipeline

model = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def get_sentiment(text):
    return model(text[:512])[0]["label"]
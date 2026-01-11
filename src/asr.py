import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import whisper

model = whisper.load_model("base")

def transcribe(path):
    return model.transcribe(path)["text"]
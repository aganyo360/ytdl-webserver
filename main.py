from fastapi import FastAPI
import yt_dlp
import os

app = FastAPI()

@app.get("/")
def home():
    return {"message": "YT-DLP Webserver is running 🎉"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/download")
def download(url: str):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)  # don’t download, just info
    return {
        "title": info.get("title"),
        "url": info.get("webpage_url"),
        "duration": info.get("duration"),
    }

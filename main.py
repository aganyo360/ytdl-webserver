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

@app.get("/download-audio")
def download_audio(url: str):
    """Download audio and return an MP3 file."""
    temp_filename = f"/tmp/{uuid.uuid4()}.mp3"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': temp_filename,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return FileResponse(
        temp_filename,
        media_type="audio/mpeg",
        filename=os.path.basename(temp_filename),
    )

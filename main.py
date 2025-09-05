from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import yt_dlp
import os
import uuid   

app = FastAPI()

@app.get("/")
def home():
    return {"message": "YT-DLP Webserver is running 🎉"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/download-audio")
def download_audio(url: str):
    """Download audio and return an MP3 file."""
    temp_filename = f"/tmp/{uuid.uuid4()}.mp3"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': temp_filename.replace(".mp3", ""),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not os.path.exists(temp_filename):
        raise HTTPException(status_code=500, detail="Audio file was not created")

    return FileResponse(
        temp_filename,
        media_type="audio/mpeg",
        filename=os.path.basename(temp_filename),
    )

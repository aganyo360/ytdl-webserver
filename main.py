from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
import yt_dlp
import uuid
import os

app = FastAPI()

@app.get("/")
def root():
    return {"message": "YouTube Downloader API is live 🚀"}

@app.get("/download")
def download_metadata(url: str = Query(..., description="YouTube video URL")):
    """Fetch metadata only (title, url, duration)."""
    ydl_opts = {"quiet": True, "skip_download": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    return {
        "title": info.get("title"),
        "url": url,
        "duration": info.get("duration")
    }

@app.get("/download-audio")
def download_audio(url: str = Query(..., description="YouTube video URL")):
    """Download and return MP3 audio (auto cleans up)."""
    temp_filename = f"/tmp/{uuid.uuid4()}.mp3"
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": temp_filename,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "audio")

        headers = {
            "Content-Disposition": f'attachment; filename="{title}.mp3"'
        }

        # Serve file, auto delete after response
        return FileResponse(
            temp_filename,
            media_type="audio/mpeg",
            filename=f"{title}.mp3",
            headers=headers,
            background=lambda: os.remove(temp_filename) if os.path.exists(temp_filename) else None
        )

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

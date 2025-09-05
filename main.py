# main.py
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
import yt_dlp
import os
import uuid

app = FastAPI()

@app.get("/api/info")
async def get_info(url: str = Query(...)):
    try:
        ydl_opts = {"quiet": True, "skip_download": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        return info
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/api/download")
async def download(url: str = Query(...), format: str = "mp3"):
    try:
        filename = f"/tmp/{uuid.uuid4()}.%(ext)s"
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": filename,
            "postprocessors": [
                {"key": "FFmpegExtractAudio", "preferredcodec": format}
            ],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            final_file = ydl.prepare_filename(info)
            if final_file.endswith(".webm") or final_file.endswith(".m4a"):
                final_file = final_file.rsplit(".", 1)[0] + f".{format}"
        return FileResponse(final_file, filename=os.path.basename(final_file))
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

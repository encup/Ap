from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
import yt_dlp
import uvicorn

app = FastAPI()

# Halaman Depan (HTML)
@app.get("/")
def home():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Video Downloader</title>
        <style>
            body { font-family: sans-serif; max-width: 600px; margin: 50px auto; text-align: center; background: #f4f4f9; }
            .card { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
            input { width: 70%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; }
            button { padding: 12px 25px; background: #6366f1; color: white; border: none; border-radius: 8px; cursor: pointer; }
            #result { margin-top: 20px; display: none; }
            img { width: 100%; border-radius: 10px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🚀 Universal Downloader</h1>
            <input type="text" id="urlInput" placeholder="Link YouTube/TikTok/IG...">
            <button onclick="getInfo()">Cari</button>
            <div id="result">
                <h3 id="title"></h3>
                <img id="thumb" src="">
                <a id="dlLink" href="#" target="_blank"><button style="background:#10b981; margin-top:10px;">Download Stream</button></a>
            </div>
        </div>
        <script>
            async function getInfo() {
                const url = document.getElementById('urlInput').value;
                const res = await fetch('/api/info', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ url: url })
                });
                const data = await res.json();
                if(data.success) {
                    document.getElementById('result').style.display = 'block';
                    document.getElementById('title').innerText = data.data.title;
                    document.getElementById('thumb').src = data.data.thumbnail;
                    document.getElementById('dlLink').href = data.data.stream_url;
                } else { alert('Gagal: ' + data.detail); }
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# API Endpoint
class VideoRequest(BaseModel):
    url: str

@app.post("/api/info")
def get_video_info(request: VideoRequest):
    ydl_opts = {'format': 'best', 'quiet': True, 'no_warnings': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(request.url, download=False)
            if not info: raise HTTPException(status_code=404, detail="Video not found")
            return {
                "success": True,
                "data": {
                    "title": info.get('title'),
                    "thumbnail": info.get('thumbnail'),
                    "stream_url": info.get('url')
                }
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

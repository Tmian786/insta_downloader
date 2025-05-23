from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import instaloader

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/download")
async def download_instagram(url: str):
    try:
        L = instaloader.Instaloader()
        shortcode = url.strip("/").split("/")[-1]  # More robust shortcode extraction
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        download_url = post.video_url if post.is_video else post.url
        return JSONResponse({"status": "success", "download_url": download_url})
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

# No need to run locally for deployment — hosting platform handles it
# To run locally, use: uvicorn main:app --reload

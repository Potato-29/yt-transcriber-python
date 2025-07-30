from fastapi import FastAPI, Request
import uvicorn
from groq import Groq     
from dotenv import load_dotenv
import os
from pytube import YouTube

from pytubefix import YouTube
from pytubefix.cli import on_progress


load_dotenv()
app = FastAPI()

@app.get("/test")
def test_endpoint():
    return {"message": "Test endpoint working!"}

@app.get("/get-transcript")

@app.post("/get-transcript")
async def get_transcript(request: Request):
    data = await request.json()
    video_url = data.get("video_url")
    print(os.getenv("GROQ_API_KEY"))
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    yt_url = "https://youtu.be/" + video_url
  

    yt = YouTube(yt_url, use_po_token=True,token_file="po_token.json")
    print(yt.title)

    ys = yt.streams.get_audio_only()
    ys.download(output_path=".", filename="audio.mp4")
    


    response = client.audio.transcriptions.create(
        file=open("audio.mp4", "rb"),
        model="whisper-large-v3-turbo",
        response_format="json"
    )
    
    return {"transcript": response.text}
def main():
    print("Hello from yt-vid-transcriber!")


if __name__ == "__main__":
    main()
    uvicorn.run(app, host="127.0.0.1", port=5000)

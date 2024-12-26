from fastapi import FastAPI, HTTPException, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import os
import requests
import urllib.parse
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for your domain
    allow_methods=["*"],
    allow_headers=["*"],
)

# PlayNote API configuration
PLAYNOTE_API_URL = "https://api.play.ai/api/v1/playnotes"
api_key = os.getenv("PLAYDIALOG_API_KEY")
user_id = os.getenv("PLAYDIALOG_USER_ID")

headers = {
    'AUTHORIZATION': api_key,
    'X-USER-ID': user_id,
    'accept': 'application/json'
}

@app.post("/generate_audio/")
def generate_audio(source_file: UploadFile = File(...)):
    """
    Accepts a PDF file and generates PlayNote audio.
    """
    try:
        # Save the uploaded file locally
        file_location = f"temp_{source_file.filename}"
        with open(file_location, "wb") as f:
            f.write(source_file.file.read())

        # Prepare file for upload
        with open(file_location, "rb") as file_to_upload:
            files = {
                'sourceFile': (source_file.filename, file_to_upload, 'application/pdf'),
                'synthesisStyle': (None, 'podcast'),
                'voice1': (None, 's3://voice-cloning-zero-shot/baf1ef41-36b6-428c-9bdf-50ba54682bd8/original/manifest.json'),
                'voice1Name': (None, 'Angelo'),
                'voice2': (None, 's3://voice-cloning-zero-shot/e040bd1b-f190-4bdb-83f0-75ef85b18f84/original/manifest.json'),
                'voice2Name': (None, 'Deedee'),
            }

            # Send request to PlayNote API
            response = requests.post(PLAYNOTE_API_URL, headers=headers, files=files)
        
        if response.status_code != 201:
            raise HTTPException(status_code=400, detail=f"Failed to generate PlayNote: {response.text}")

        playNoteId = response.json().get('id')
        double_encoded_id = urllib.parse.quote(playNoteId, safe='')
        status_url = f"{PLAYNOTE_API_URL}/{double_encoded_id}"

        # Poll for completion
        while True:
            response = requests.get(status_url, headers=headers)
            if response.status_code == 200:
                playnote_data = response.json()
                status = playnote_data['status']
                if status == 'completed':
                    audio_url = playnote_data['audioUrl']
                    return JSONResponse(content={"audio_url": audio_url, "message": "PlayNote generation complete!"})
                elif status == 'generating':
                    time.sleep(10)  # Shorter polling time for web app
                else:
                    raise HTTPException(status_code=500, detail="PlayNote generation failed.")
            else:
                raise HTTPException(status_code=500, detail="Error polling for PlayNote status.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up the temporary file
        if os.path.exists(file_location):
            os.remove(file_location)



#download audio file
@app.get("/download_audio/")
def download_audio(audio_url: str):
    """
    Downloads the generated audio file using the provided audio_url and serves it for browser download.
    """
    try:
        response = requests.get(audio_url)
        if response.status_code == 200:
            audio_data = io.BytesIO(response.content)
            audio_data.seek(0)  # Ensure the stream is at the beginning
            return StreamingResponse(
                audio_data,
                media_type="audio/wav",
                headers={"Content-Disposition": "attachment; filename=output.wav"}
            )
        else:
            raise HTTPException(status_code=400, detail="Failed to download audio.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

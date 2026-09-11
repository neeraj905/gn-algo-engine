from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, HTMLResponse
import shutil
import os

app = FastAPI(title="AI Video Studio Engine")

# Directories setup
os.makedirs("temp_uploads", exist_ok=True)
os.makedirs("output", exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head>
            <title>AI Video Studio</title>
            <style>
                body { font-family: Arial, sans-serif; background: #0f172a; color: #fff; padding: 30px; }
                .container { max-width: 600px; margin: auto; background: #1e293b; padding: 20px; border-radius: 8px; }
                input, textarea, button { width: 100%%; margin-top: 10px; padding: 10px; background: #0f172a; color: #fff; border: 1px solid #475569; border-radius: 4px; }
                button { background: #2563eb; cursor: pointer; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>AI Video & Character Editor</h2>
                <form action="/api/comment-to-video" method="post" enctype="multipart/form-data">
                    <label>1. Upload Video:</label>
                    <input type="file" name="video" accept="video/*" required>
                    
                    <label>2. Upload Target Face Photo:</label>
                    <input type="file" name="target_face" accept="image/*" required>
                    
                    <label>3. AI Character Comment / Prompt:</label>
                    <textarea name="comment_text" rows="3" placeholder="E.g., Say hello and run like this..." required></textarea>
                    
                    <button type="submit">Run AI Pipeline</button>
                </form>
            </div>
        </body>
    </html>
    """

@app.post("/api/comment-to-video")
async def comment_to_video(
    video: UploadFile = File(...),
    target_face: UploadFile = File(...),
    comment_text: str = Form(...),
    target_gender: str = Form("female")
):
    video_path = f"temp_uploads/{video.filename}"
    face_path = f"temp_uploads/{target_face.filename}"
    
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)
    with open(face_path, "wb") as buffer:
        shutil.copyfileobj(target_face.file, buffer)
        
    print(f"[AI PIPELINE] Comment received: {comment_text}")
    
    output_file_name = f"processed_{video.filename}"
    output_path = f"output/{output_file_name}"
    
    # Filhal testing ke liye input video ko hi output mana gaya hai
    shutil.copy(video_path, output_path)

    return {
        "status": "success",
        "message": f"Successfully processed with prompt: '{comment_text}'",
        "download_url": f"/download/{output_file_name}"
    }

@app.get("/download/{filename}")
async def download_file(filename: str):
    return FileResponse(f"output/{filename}")
        

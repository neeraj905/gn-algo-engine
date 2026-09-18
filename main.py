import os
import subprocess
import urllib.request
from gtts import gTTS
import streamlit as st
import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis

st.set_page_config(page_title="AI Video Studio", page_icon="🎬")
st.title("🎬 AI Video & Face Swap + Voice Merger")

st.header("1. Upload Video & Target Face")
video_file = st.file_uploader("Upload Main Video", type=["mp4", "mov"])
image_file = st.file_uploader("Upload Target Face Image", type=["jpg", "png"])

st.header("2. Text to Speech (TTS)")
user_text = st.text_area("Enter Text for Voiceover", "Hello, this is my AI generated voice.")

if st.button("Generate & Merge Video"):
    if video_file and image_file and user_text:
        progress_bar = st.progress(0)
        status_text = st.empty()
        status_text.text("Processing... Saving files.")

        # Save uploaded video
        input_video_path = "input_video.mp4"
        with open(input_video_path, "wb") as f:
            f.write(video_file.getbuffer())

        # Save uploaded image
        target_face_path = "target_face.jpg"
        with open(target_face_path, "wb") as f:
            f.write(image_file.getbuffer())

        # Generate TTS Audio
        tts = gTTS(text=user_text, lang='en')
        audio_path = "tts_audio.mp3"
        tts.save(audio_path)

        status_text.text("Loading AI Face Swap models (pehle run par model download hone mein thoda time lag sakta hai)...")
        
        # Download inswapper model if not exists
        model_path = "inswapper_128.onnx"
        if not os.path.exists(model_path):
            status_text.text("Downloading face swapper model (~500MB)... Please wait.")
            url = "https://huggingface.co/ezioruan/inswapper_128.onnx/resolve/main/inswapper_128.onnx"
            try:
                urllib.request.urlretrieve(url, model_path)
            except Exception as e:
                st.error(f"Failed to download model: {e}")

        try:
            # Initialize InsightFace
            app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
            app.prepare(ctx_id=0, det_size=(640, 640))
            swapper = insightface.model_zoo.get_model(model_path, download=False, download_zip=False)

            # Read target face
            target_img = cv2.imread(target_face_path)
            target_faces = app.get(target_img)
            
            if len(target_faces) == 0:
                st.error("No face detected in the uploaded target image! Please upload a clear, front-facing image.")
            else:
                target_face = target_faces[0]

                # Process Video Frames
                status_text.text("Swapping faces frame-by-frame across the video...")
                cap = cv2.VideoCapture(input_video_path)
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

                temp_output_video = "temp_swapped.mp4"
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(temp_output_video, fourcc, fps if fps > 0 else 24, (width, height))

                frame_count = 0
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    # Detect and swap faces in current frame
                    faces = app.get(frame)
                    res_frame = frame.copy()
                    for face in faces:
                        res_frame = swapper.get(res_frame, face, target_face, paste_back=True)
                    
                    out.write(res_frame)
                    frame_count += 1
                    if total_frames > 0:
                        progress_bar.progress(min(frame_count / total_frames, 1.0))

                cap.release()
                out.release()

                # Merge with audio using FFmpeg
                status_text.text("Merging audio and finalizing video...")
                output_path = "final_output.mp4"
                cmd = f"ffmpeg -y -i {temp_output_video} -i {audio_path} -c:v libx264 -c:a aac -map 0:v:0 -map 1:a:0 {output_path}"
                subprocess.run(cmd, shell=True)

                if os.path.exists(output_path):
                    status_text.text("Done!")
                    st.success("Video Processed Successfully with Face Swap & Voice!")
                    st.video(output_path)
                else:
                    st.error("Error in merging video with FFmpeg.")

        except Exception as ex:
            st.error(f"An error occurred during face swapping: {ex}")

    else:
        st.warning("Please upload both video, target face image, and enter text!")

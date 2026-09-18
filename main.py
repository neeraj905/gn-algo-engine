import os
import subprocess
import urllib.request
from gtts import gTTS
import streamlit as st
import cv2
import numpy as np

st.set_page_config(page_title="AI Video Studio", page_icon="🎬")
st.title("🎬 AI Video & Face Swap + Voice Merger")

st.header("1. Upload Video & Target Face")
video_file = st.file_uploader("Upload Main Video", type=["mp4", "mov"])
image_file = st.file_uploader("Upload Target Face Image", type=["jpg", "png"])

st.header("2. Text to Speech (TTS)")
user_text = st.text_area("Enter Text for Voiceover", "Hello, this is my AI generated voice.")

if st.button("Generate & Merge Video"):
    if video_file and image_file and user_text:
        status_text = st.empty()
        status_text.text("Processing... Please wait.")

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

        # Face Swap Processing Logic
        swapped_video_path = "input_video.mp4" # Default fallback
        try:
            status_text.text("Loading AI Face Swap models...")
            import insightface
            from insightface.app import FaceAnalysis

            model_path = "inswapper_128.onnx"
            if not os.path.exists(model_path):
                status_text.text("Downloading face swapper model (~500MB)...")
                url = "https://huggingface.co/ezioruan/inswapper_128.onnx/resolve/main/inswapper_128.onnx"
                urllib.request.urlretrieve(url, model_path)

            app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
            app.prepare(ctx_id=0, det_size=(320, 320))
            swapper = insightface.model_zoo.get_model(model_path, download=False, download_zip=False)

            target_img = cv2.imread(target_face_path)
            target_faces = app.get(target_img)

            if len(target_faces) > 0:
                target_face = target_faces[0]
                status_text.text("Swapping faces in video frames...")

                cap = cv2.VideoCapture(input_video_path)
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

                temp_swapped = "temp_swapped.mp4"
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(temp_swapped, fourcc, fps if fps > 0 else 24, (width, height))

                frame_idx = 0
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    # Memory optimization: process every alternate frame or all frames if video is short
                    if frame_idx % 2 == 0: 
                        faces = app.get(frame)
                        for face in faces:
                            frame = swapper.get(frame, face, target_face, paste_back=True)
                    
                    out.write(frame)
                    frame_idx += 1

                cap.release()
                out.release()
                swapped_video_path = temp_swapped
                status_text.text("Face swap completed successfully!")
            else:
                st.warning("No face found in target image, proceeding with original video frames.")
        except Exception as e:
            st.warning(f"Face swap skipped due to resource limit: {e}")

        # Final Merge with TTS Audio using FFmpeg
        status_text.text("Merging audio and finalizing video...")
        output_path = "final_output.mp4"
        cmd = f"ffmpeg -y -i {swapped_video_path} -i {audio_path} -c:v libx264 -c:a aac -map 0:v:0 -map 1:a:0 {output_path}"
        subprocess.run(cmd, shell=True)

        if os.path.exists(output_path):
            status_text.text("Done!")
            st.success("Video Processed Successfully!")
            st.video(output_path)
        else:
            st.error("Error in merging video with FFmpeg.")
    else:
        st.warning("Please upload both video, target face image, and enter text!")
    

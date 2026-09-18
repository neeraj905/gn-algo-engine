import os
import subprocess
from gtts import gTTS
import streamlit as st
import cv2
import numpy as np

st.set_page_config(page_title="AI Video Studio", page_icon="🎬")
st.title("🎬 AI Video & Voice Merger")

st.header("1. Upload Video & Target Face")
video_file = st.file_uploader("Upload Main Video", type=["mp4", "mov"])
image_file = st.file_uploader("Upload Target Face Image", type=["jpg", "png"])

st.header("2. Text to Speech (TTS)")
user_text = st.text_area("Enter Text for Voiceover", "Hello, this is my AI generated voice.")

if st.button("Generate & Merge Video"):
    if video_file and image_file and user_text:
        st.info("Processing... Please wait.")

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

        # Safe Face-Swap check (Preventing server crash due to memory limits)
        try:
            import insightface
            from insightface.app import FaceAnalysis
            st.info("InsightFace library detected. Initializing face detection...")
            # Agar yahan memory ya compatibility issue hoga toh except block mein chala jayega
        except Exception as e:
            st.warning(f"Note: Face swap module skipped due to server environment limitation: {e}")

        # Final Output Path using FFmpeg for video + generated audio merge
        output_path = "final_output.mp4"
        cmd = f"ffmpeg -y -i {input_video_path} -i {audio_path} -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 {output_path}"
        subprocess.run(cmd, shell=True)

        if os.path.exists(output_path):
            st.success("Video Processed Successfully with Voiceover!")
            st.video(output_path)
        else:
            st.error("Error in processing video with FFmpeg.")
    else:
        st.warning("Please upload both video, target face image, and enter text!")

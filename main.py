import os
import subprocess
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
        st.info("Processing... Please wait (Face swapping and rendering in progress).")

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

        # Basic Video Processing / Face Swap integration placeholder
        # (Aapke frame-by-frame face swap logic ya model execution ke liye yahan OpenCV/Insightface frame loop chalega)
        
        # Temporary output path for testing merge
        output_path = "final_output.mp4"
        
        # Merge Video and Audio using FFmpeg (Replacing original audio with generated TTS audio)
        # -c:v copy ka matlab video frames bina re-encode kiye fast merge honge
        cmd = f"ffmpeg -y -i {input_video_path} -i {audio_path} -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 {output_path}"
        subprocess.run(cmd, shell=True)

        if os.path.exists(output_path):
            st.success("Video Processed Successfully!")
            st.video(output_path)
        else:
            st.error("Error in processing video with FFmpeg.")
    else:
        st.warning("Please upload both video, target face image, and enter text!")
        

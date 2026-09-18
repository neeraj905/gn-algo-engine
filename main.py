import os
import subprocess
from gtts import gTTS
import streamlit as st

st.set_page_config(page_title="AI Video Studio", layout="centered")
st.title("🎬 AI Video & Voice Merger")

st.header("1. Upload Video & Target Face")
video_file = st.file_uploader("Upload Main Video", type=["mp4", "mov"])
image_file = st.file_uploader("Upload Target Face Image", type=["jpg", "png", "jpeg"])

st.header("2. Text to Speech (TTS)")
user_text = st.text_area("Enter Text for Voiceover", "Hello, this is my AI generated voice.")

if st.button("Generate & Merge Video"):
    if video_file and image_file and user_text:
        st.info("Processing... Please wait.")
        
        # Save uploaded video
        with open("input_video.mp4", "wb") as f:
            f.write(video_file.getbuffer())
            
        # Save uploaded image
        with open("target_face.jpg", "wb") as f:
            f.write(image_file.getbuffer())
            
        # Generate TTS Audio
        tts = gTTS(text=user_text, lang='en')
        tts.save("tts_audio.mp3")
        
        # Merge Video and Audio using FFmpeg
        output_path = "final_output.mp4"
        cmd = f"ffmpeg -y -i input_video.mp4 -i tts_audio.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 {output_path}"
        subprocess.run(cmd, shell=True)
        
        if os.path.exists(output_path):
            st.success("Video Processed Successfully!")
            st.video(output_path)
        else:
            st.error("Error in processing video with FFmpeg.")
    else:
        st.warning("Please upload both video, image and enter text.")
                  

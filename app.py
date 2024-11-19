import streamlit as st
import os

# Set up the app title
st.title("TTS MOS Evaluation")

# Instructions for participants
st.write("Please listen to the audio samples below and rate them on a scale of 1 (Bad) to 5 (Excellent).")

# Directory containing audio files
audio_dir = "audio_files"  # Replace with your audio file directory

# List all audio files
audio_files = sorted([f for f in os.listdir(audio_dir) if f.endswith('.mp3') or f.endswith('.wav')])

# Initialize scores dictionary
scores = {}

# Loop through and display each audio file
for audio_file in audio_files:
    st.write(f"Audio: {audio_file}")
    audio_path = os.path.join(audio_dir, audio_file)
    st.audio(audio_path)

    # Rating slider
    score = st.slider(f"Rate {audio_file}", min_value=1, max_value=5, key=audio_file)
    scores[audio_file] = score

# Submit button
if st.button("Submit Ratings"):
    # Save the results to a file
    with open("ratings.csv", "a") as f:
        for audio_file, score in scores.items():
            f.write(f"{audio_file},{score}\n")
    st.success("Thank you for your feedback!")

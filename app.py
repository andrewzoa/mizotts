import streamlit as st
import os
import subprocess
import pandas as pd

# Set up the app title
st.title("TTS MOS Evaluation")

# Instructions for participants
st.write("Please listen to the audio samples below and rate them on a scale of 1 (Bad) to 5 (Excellent).")

# Function to clone the repository (if not already cloned)
def clone_repo():
    repo_url = "https://github.com/andrewzoa/mizotts.git"  # Your repo URL
    repo_dir = "mizotts"  # Local directory where the repo should be cloned

    if not os.path.exists(repo_dir):
        st.write(f"Cloning repository from {repo_url}...")
        try:
            # Clone the repository if it doesn't exist
            subprocess.run(['git', 'clone', repo_url, repo_dir], check=True)
            st.success("Repository cloned successfully!")
        except Exception as e:
            st.error(f"Error cloning repository: {e}")
    else:
        st.write(f"Repository already cloned at {repo_dir}.")

# Clone repository at the start
clone_repo()

# Directory containing audio files (adjust as necessary)
audio_dir = "audio_files"  # Replace with your audio file directory

# List all audio files
audio_files = sorted([f for f in os.listdir(audio_dir) if f.endswith('.mp3') or f.endswith('.wav')])

# Initialize scores dictionary in session state if it doesn't exist
if 'scores' not in st.session_state:
    st.session_state.scores = {}

# Loop through and display each audio file
for audio_file in audio_files:
    st.write(f"Audio: {audio_file}")
    audio_path = os.path.join(audio_dir, audio_file)
    st.audio(audio_path)

    # Rating slider
    score = st.slider(f"Rate {audio_file}", min_value=1, max_value=5, key=audio_file)
    st.session_state.scores[audio_file] = score

# Submit button
if st.button("Submit Ratings"):
    # Convert the stored ratings to a DataFrame
    df = pd.DataFrame(list(st.session_state.scores.items()), columns=['Audio', 'Rating'])

    # Display the ratings on the page
    st.write("### Submitted Ratings")
    st.write(df)

    # Optionally, save ratings to a CSV file (local to the app)
    ratings_file = 'ratings.csv'
    if os.path.exists(ratings_file):
        df.to_csv(ratings_file, mode='a', header=False, index=False)
    else:
        df.to_csv(ratings_file, index=False)

    st.success("Thank you for your feedback! Ratings have been saved locally.")


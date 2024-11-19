import streamlit as st
import git
import os
import subprocess
import pandas as pd  # Import pandas

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
    # Path to your cloned GitHub repository
    repo_path = './mizotts'  # This assumes the repo is cloned into the current working directory

    # Initialize Git repository
    try:
        repo = git.Repo(repo_path)
    except git.exc.NoSuchPathError:
        st.error(f"Git repository not found at {repo_path}. Please check the path.")
    
    # Create a DataFrame from the ratings
    df = pd.DataFrame(list(scores.items()), columns=['Audio', 'Rating'])
    
    # Define the path for ratings.csv in the repository
    ratings_file = os.path.join(repo_path, 'ratings.csv')

    # Check if the directory exists, if not, create it
    ratings_dir = os.path.dirname(ratings_file)
    if not os.path.exists(ratings_dir):
        os.makedirs(ratings_dir)

    # If ratings.csv doesn't exist, create it with headers
    if not os.path.exists(ratings_file):
        df.to_csv(ratings_file, index=False)
    else:
        # Append new ratings to the existing file
        df.to_csv(ratings_file, mode='a', header=False, index=False)

    # Stage, commit, and push changes
    try:
        repo.git.add('ratings.csv')
        repo.git.commit('-m', 'Update ratings')
        repo.git.push('origin', 'main')
        st.success("Thank you for your feedback! Ratings saved and pushed to GitHub!")
    except Exception as e:
        st.error(f"Error pushing to GitHub: {e}")

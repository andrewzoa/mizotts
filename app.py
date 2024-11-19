import streamlit as st
import os
import git
import pandas as pd

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
    # Path to your cloned GitHub repository
    repo_path = '/mizotts'  # Change this to your local repository path

    # Initialize Git repository
    repo = git.Repo(repo_path)

    # Create a DataFrame from the ratings
    df = pd.DataFrame(list(scores.items()), columns=['Audio', 'Rating'])
    
    # Define the path for ratings.csv in the repository
    ratings_file = os.path.join(repo_path, 'ratings.csv')

    # If ratings.csv doesn't exist, create it with headers
    if not os.path.exists(ratings_file):
        df.to_csv(ratings_file, index=False)
    else:
        # Append new ratings to the existing file
        df.to_csv(ratings_file, mode='a', header=False, index=False)

    # Stage, commit, and push changes
    repo.git.add('ratings.csv')
    repo.git.commit('-m', 'Update ratings')
    repo.git.push('origin', 'main')

    st.success("Thank you for your feedback! Ratings saved and pushed to GitHub!")

import streamlit as st
import os
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
    # Save the results to a file
    with open("ratings.csv", "a") as f:
        for audio_file, score in scores.items():
            f.write(f"{audio_file},{score}\n")
    st.success("Thank you for your feedback!")



# Path to your cloned GitHub repository
repo_path = '/mizotts'  # Change this to your local repository path

# Initialize Git repository
repo = git.Repo(repo_path)

# Function to save ratings and push to GitHub
def save_and_push_to_github(df):
    # Save ratings to CSV
    ratings_file = os.path.join(repo_path, 'ratings.csv')
    df.to_csv(ratings_file, index=False)

    # Stage, commit, and push changes
    repo.git.add('ratings.csv')
    repo.git.commit('-m', 'Update ratings')
    repo.git.push('origin', 'main')

    st.success("Ratings saved and pushed to GitHub!")

# Collect ratings and save
if st.button("Submit Ratings"):
    df = pd.DataFrame(list(scores.items()), columns=['Audio', 'Rating'])
    save_and_push_to_github(df)

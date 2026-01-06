import time
import shutil
import os
import re
from database import add_movie
import streamlit as st

SAMPLE_VIDEO_SOURCE = "sample_video.mp4"
GENERATED_DIR = "generated_movies"

if not os.path.exists(GENERATED_DIR):
    os.makedirs(GENERATED_DIR)

def sanitize_filename(filename):
    """
    Sanitizes the filename to prevent directory traversal and special chars.
    """
    # Remove characters that aren't alphanumerics, underscores, hyphens or spaces
    s = re.sub(r'[^a-zA-Z0-9_\-\s]', '', filename)
    # Replace spaces with underscores
    s = s.replace(' ', '_')
    return s

def generate_movie(user_email, title, genre, style, year):
    """
    Simulates AI video generation.
    1. Shows a progress bar.
    2. Copies the sample video to a new path.
    3. Saves entry to DB.
    """

    # Simulation UI
    progress_text = "AI Showrunner is crafting your scene..."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.03) # Simulate work (3 seconds total)
        my_bar.progress(percent_complete + 1, text=progress_text)

    my_bar.empty()

    # "Generation" (Copying file)
    # Security fix: Sanitize title
    safe_title = sanitize_filename(title)
    filename = f"{int(time.time())}_{safe_title}.mp4"
    destination_path = os.path.join(GENERATED_DIR, filename)

    # Ensure source exists (downloaded in step 1)
    if os.path.exists(SAMPLE_VIDEO_SOURCE):
        shutil.copy(SAMPLE_VIDEO_SOURCE, destination_path)
    else:
        # Fallback if sample missing
        with open(destination_path, 'w') as f:
            f.write("Mock Video Content")

    # Save to DB
    add_movie(user_email, title, genre, style, year, destination_path)

    return destination_path

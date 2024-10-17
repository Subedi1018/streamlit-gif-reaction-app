import streamlit as st
import requests
from transformers import pipeline
import random

# Load the emotion analysis model
emotion_analysis = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

# Function to map emotion to Giphy queries
def map_emotion_to_query(emotion):
    if emotion == "joy":
        return "happy, excited, cheerful"
    elif emotion == "anger":
        return "angry, frustrated, mad"
    elif emotion == "sadness":
        return "sad, crying, upset"
    elif emotion == "fear":
        return "scared, fearful, terrified"
    elif emotion == "neutral":
        return "meh, bored, calm"
    else:
        return emotion  # Use the raw emotion if none match

# Function to get a random GIF from Giphy for a given emotion
def get_gif(emotion):
    api_key = "kLj0T0EGqhseKSlAP3s0lE1y0L0L6JbZ"
    query = map_emotion_to_query(emotion)
    
    # Fetch multiple GIFs from Giphy (limit=10 for more variety)
    url = f"https://api.giphy.com/v1/gifs/search?api_key={api_key}&q={query}&limit=10"
    response = requests.get(url).json()
    
    # Randomly select one GIF from the returned data
    gifs = response['data']
    random_gif = random.choice(gifs)  # Pick a random GIF from the list
    gif_url = random_gif['images']['original']['url']
    
    return gif_url

# Streamlit App Title
st.title("Real-Time GIF Reaction Generator")

# Get user input
user_input = st.text_input("How are you feeling?", "")

# Variable to store the last detected emotion
if 'last_emotion' not in st.session_state:
    st.session_state.last_emotion = None

# Button to analyze the emotion and display GIF
if st.button("Analyze Emotion"):
    if user_input:
        result = emotion_analysis(user_input)[0]
        emotion = result['label'].lower()
        st.session_state.last_emotion = emotion  # Store the detected emotion
        st.write(f"Emotion detected: {emotion} (confidence: {result['score']:.2f})")
        
        # Get and display a random GIF for the detected emotion
        gif_url = get_gif(emotion)
        st.image(gif_url)
    else:
        st.write("Please enter a feeling.")

# Button to refresh the GIF for the same emotion
if st.session_state.last_emotion:
    if st.button("Get Another GIF"):
        gif_url = get_gif(st.session_state.last_emotion)
        st.image(gif_url)


import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set page title and favicon
st.set_page_config(page_title="Spotify-like Uploader", page_icon=":musical_note:")

# Define CSS for styling
st.markdown(
    """
    <style>
    .title {
        text-align: center;
        color: #1DB954;
        font-size: 36px;
        margin-bottom: 30px;
    }
    .upload-box {
        border: 2px dashed #1DB954;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
    }
    .upload-button {
        display: block;
        margin: 0 auto;
        background-color: #1DB954;
        color: white;
        font-weight: bold;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .upload-button:hover {
        background-color: #25b84c;
    }
    .description {
        text-align: center;
        color: #1DB954;
        font-size: 18px;
        margin-top: 50px;
        margin-bottom: 20px;
    }
    .example-graphs {
        display: flex;
        justify-content: space-around;
        align-items: center;
        margin-bottom: 50px;
    }
    .example-graph {
        flex: 1;
        margin: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# App title
st.markdown("<h1 class='title'>Do you wanna know... how popular your song will be?</h1>", unsafe_allow_html=True)

# Paste link section
paste_link = st.text_input("Paste link to your song", key="song_link")

# Upload button
if paste_link:
    st.success(f"Link pasted successfully! Link: {paste_link}")

# Description of AI-powered tool
st.markdown("<h2 class='description'>An AI-powered tool to predict song popularity using nearest neighbors</h2>", unsafe_allow_html=True)

# Example graphs
st.markdown("<div class='example-graphs'>", unsafe_allow_html=True)

# Example graph 1
with st.markdown("<div class='Performance measure'>", unsafe_allow_html=True):
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    plt.figure(facecolor='#040f13')  
    plt.plot(x, y, color='#1DB954')
    plt.title("Example Graph 1")
    st.pyplot(plt)


# Example graph 2
with st.markdown("<div class='Samples'>", unsafe_allow_html=True):
    x = np.linspace(0, 10, 100)
    y = np.cos(x)
    plt.figure(facecolor='#040f13')
    plt.plot(x, y, color='#1DB954')
    plt.title("Example Graph 2")
    st.pyplot(plt)

st.markdown("</div>", unsafe_allow_html=True)  # Close example-graphs div

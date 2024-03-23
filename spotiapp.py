<<<<<<< HEAD
# Libraries

## Data
import pandas as pd
import numpy as np

## Vis
import matplotlib.pyplot as plt
import streamlit as st

## Spotiy API
import spotipy

## Modules
import re
import os

## Env
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
dotenv_path = r'C:\Users\santi\OneDrive\Desktop\Spotify_Popularity\.env.txt'
load_dotenv(dotenv_path)

## Models
import pickle
import joblib

# Functions

def obtener_uri_desde_enlace(enlace):
    # Expresión regular para buscar el URI en el enlace de Spotify
    patron = r'^https://open\.spotify\.com/track/([a-zA-Z0-9]+)'
    coincidencia = re.match(patron, enlace)
    
    # Si hay coincidencia, devuelve el URI del track, de lo contrario devuelve None
    if coincidencia:
        return coincidencia.group(1)
    else:
        return None
    
def analyze_audio_features(tablon):
    comments = []
    
    # Define thresholds and comments for each audio feature
    thresholds_comments = {
        "acousticness": (0.6, "is mainly acoustic"),
        "danceability": (0.6, "is danceable"),
        "energy": (0.6, "is energetic"),
        "instrumentalness": (0.6, "exhibits an instrumental essence"),
        "valence": (0.6, "embodies a positive essence"),
        "liveness": (0.6, "feels as if it's performed live"),
        "speechiness": (0.6, "presents a significant amount of spoken-word elements")
    }
    
    # Get audio features from the DataFrame
    audio_features = tablon.iloc[0][["acousticness", "danceability", "energy", "instrumentalness", "valence", "liveness", "speechiness"]]
    
    # Iterate over audio features and compare with thresholds
    for feature, value in audio_features.items():
        threshold, comment = thresholds_comments.get(feature, (None, None))
        if threshold is not None and value > threshold:
            comments.append(comment)
    
    # Concatenate comments if more than one
    final_comment = ", ".join(comments)
    if final_comment:
        final_comment = f"The song {final_comment}."
    
    return final_comment


# Spotify Api Connection
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))


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
paste_link = st.text_input("Paste the link to your song: ", key="song_link")
# Upload button
if paste_link:
    st.success(f"We successfully found your song!!! Link: {paste_link}")

    uri = obtener_uri_desde_enlace(paste_link)

    # Track Metadata
    track = sp.track(paste_link)
    results = [track]
    track_ids = [track['id']]
    track_names = [track['name']]
    artists_names = [track['artists'][0]['name']]
    popularities = [track['popularity']]
    duration_ms = [track['duration_ms']]
    years = int(track['album']['release_date'][:4])
    data = {
        'id': track_ids,
        'name': track_names,
        'artist': artists_names,
        'popularity': popularities,
        'duration_ms': duration_ms,
        'year': years,
    }

    df = pd.DataFrame(data)

    # Track Audio Features
    audio_features = sp.audio_features(track_ids[0])
    df_audio_features = pd.DataFrame(audio_features)
    df_audio_features = df_audio_features.drop(['type', 'uri', 'track_href', 'analysis_url', 'duration_ms'], axis=1)

    # Merge metadata and audio features
    tabloncito = pd.merge(df, df_audio_features, how = 'left', left_on = 'id', right_on = 'id')

    st.write(tabloncito)
    preview_url = sp.track(uri)['preview_url']

    # Reproducir el fragmento de la canción si hay una vista previa disponible
    if preview_url:
        st.audio(preview_url, format='audio/ogg', start_time=30)  # Comienza la reproducción desde el segundo 30
    else:
        st.write("Lo siento, no hay vista previa disponible para esta canción.")
    # Image
    imagen_url = track['album']['images'][0]['url']

    # Diseño de columnas para mostrar la imagen y las características de la canción al lado
    
    col1, col2 = st.columns([1, 2])

    # Mostrar la imagen en la primera columna
    with col1:
        st.image(imagen_url,  width=200)

    # Mostrar las características de la canción en la segunda columna
    with col2:
        st.write("Title: ", track_names[0])
        st.write("Artist: ", artists_names[0])
        st.write("Release Year: ", years)
        final_comment = analyze_audio_features(tabloncito)
        if final_comment:
            st.write(final_comment)
        else:
            st.write("None of the audio features have a value high enough to categorize the song.")

    # ML Model
    ruta_archivo_pkl = 'modelo_knn.pkl'
    with open(ruta_archivo_pkl, 'rb') as archivo_pkl:
        # Cargar el objeto desde el archivo .pkl
        modelo = pickle.load(archivo_pkl)

    # Scaler
    scaler = joblib.load('scaler.pkl')


    X = tabloncito[['duration_ms', 'danceability', 'key', 'loudness', 
                        'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'tempo', 'time_signature', 'popularity']]

    X_scaled = scaler.transform(X)
    modelo.predict(X_scaled)
    prediccion = modelo.predict(X_scaled)[0]
    st.write("Based on our music analysis expert, SpotiBot the Melomaniac, we can determine that your song will have a popularity score of: ", prediccion)


# Description of AI-powered tool
st.markdown("<h2 class='description'>An AI-powered tool to predict song popularity on Spotify</h2>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)  # Close example-graphs div
=======
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
>>>>>>> e1ab05eb1788c936309cf48ed50e45e549888465

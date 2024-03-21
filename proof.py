import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os
import time
dotenv_path = r'C:\Users\MAFISH\Documents\spoti\Spoti-Pop\.env.txt'
load_dotenv(dotenv_path)

# Configura tus credenciales de cliente
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

# Autenticación con Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
print(client_id)

# Obtener el ID de la playlist
dfs = []
#playlist_id = ['1M31YfWCBmOSlGGyF0wvsw', '37i9dQZF1DX4KeocBrdbJg', '37i9dQZEVXbMDoHDwVN2tF', '37i9dQZF1DXbvPjXfc8G9S',
#              '4KlHX1H41ZIyQ5oodAp2kj', '7xwYHh7KbKDtlMblSkvtfu']

playlist_id = ['7xwYHh7KbKDtlMblSkvtfu']
playlist_info = sp.playlist('7xwYHh7KbKDtlMblSkvtfu')
total_tracks = playlist_info['tracks']['total']
print(f"La lista de reproducción tiene {total_tracks} canciones.")


def divisible_by_100_list(x):
    closest_below = (x // 100) * 100
    return list(range(0, closest_below + 1, 100))

listaplaylist = divisible_by_100_list(total_tracks)

for i in listaplaylist:

    for pl in playlist_id:
        # Obtener las canciones de la playlist
        results = sp.playlist_tracks(pl,offset =i)

        #################################################################################3

        # Listas para almacenar los datos
        song_names = []
        song_ids = []
        #audio_features = []
        popularity = []
        artists = []
        release_years = []
        
        # Iterar sobre las canciones y obtener los datos
        for track in results['items']:
            # Obtener datos de la canción
            song_name = track['track']['name']
            song_id = track['track']['id']
            print(f"Processing song: {song_name}, ID: {song_id}")  # Add this line for debugging
            if song_id:
                song_names.append(song_name)
                song_ids.append(song_id)
                time.sleep(0.1)
                # Obtener popularidad de la canción
                song_popularity = track['track']['popularity']
                popularity.append(song_popularity)
            
                # Obtener género de la canción
                artist_info = track['track']['artists'][0]  # Obtener la información del primer artista de la canción
                artist_name = artist_info['name']
                artists.append(artist_name)
            
                # Obtener año de lanzamiento de la canción
                track_info = sp.track(song_id)
                release_date = track_info['album']['release_date']
                release_year = release_date.split('-')[0] if release_date else None
                release_years.append(release_year)
            else:
                print(f"Skipping song: {song_name}, ID is None")  # Add this line for debugging

    
        # Crear DataFrame con los datos
        df = pd.DataFrame({
            'Song ID': song_ids,
            'Song Name': song_names,
            'Artist Name': artists,
            'Year': release_years,
            'Popularity': popularity
        })
        
        #df_audio_features = pd.DataFrame(audio_features)
        #df_completo = pd.merge(df, df_audio_features, how='left', left_on='Song ID', right_on='id')
        #df_completo = df_completo.drop(columns=['type', 'id', 'uri', 'track_href', 'analysis_url'], axis=1)
        dfs.append(df)


tablon = pd.concat(dfs)
tablon = tablon.drop_duplicates(subset='Song ID').reset_index(drop=True)
print(tablon)
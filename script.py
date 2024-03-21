import pandas as pd
from dotenv import load_dotenv
import os
import time
dotenv_path = r'C:\Users\santi\OneDrive\Desktop\Spotify_Popularity\.env.txt'
load_dotenv(dotenv_path)

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

from minim import spotify
import pandas as pd
client = spotify.WebAPI(flow="pkce", browser=True, web_framework="http.server",
                        scopes=spotify.WebAPI.get_scopes("all"), overwrite=True)

# Specify the target Spotify playlist's ID.
playlist_id = "bff27fb8fb714104"

# Get the first 100 playlist items/tracks.
resp = client.get_playlist_items(playlist_id, limit=100)

# Get the track IDs of the returned playlist items/tracks.
track_ids = [item["track"]["id"] for item in resp["items"]]

# Get the audio features for the 100 tracks.
afs = client.get_tracks_audio_features(track_ids)

# Create a DataFrame using the audio features data.
df = pd.DataFrame(afs)

# Iterate through the rest of the playlist items/tracks.
while True:

    # Break the loop if all playlist items/tracks have been retrieved.
    if resp["offset"] + resp["limit"] >= resp["total"]:
        break

    # Same procedure as above.
    resp = client.get_playlist_items(playlist_id, limit=100, 
                                     offset=resp["offset"] + resp["limit"])
    track_ids = [item["track"]["id"] for item in resp["items"]]
    afs = client.get_tracks_audio_features(track_ids)

    # Concatenate the new audio features data to the existing DataFrame.
    df = pd.concat([df, pd.DataFrame(afs)])
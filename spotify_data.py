from dotenv import load_dotenv
import os
import json
from flask import Flask , session
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
import base64
from requests import post,get
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = "http://localhost:5000/callback"
scope = 'playlist-read-private'

cache_handler = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    cache_handler=cache_handler,
    show_dialog=True
)

sp1 = Spotify(auth_manager=sp_oauth)


sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope="user-read-playback-state"
))

# current_playback = sp.current_playback()

# if current_playback and current_playback["item"]:
#     current_track = current_playback["item"]
#     print(f"Currently Playing: {current_track['name']} by {', '.join(artist['name'] for artist in current_track['artists'])}")
# else:
#     print("No active playback found.")
    
# Function to pause music
# def pause_music():
#     if device_id:
#         sp.pause_playback(device_id=device_id)
#         print("Playback paused.")
#     else:
#         print("No active device found.")
    
# Get the active device ID
# devices = sp.devices()
# device_id = None
# if devices["devices"]:
#     device_id = devices["devices"][0]["id"]
# else:
#     print("No active devices found. Open Spotify on a device first.")
    
# pause_music()

# if device_id:
#     # Start playback with a track or playlist URI
#     sp.start_playback(device_id=device_id, uris=["spotify:track:3n3Ppam7vgaVa1iaRUc9Lp"])
#     print("Playing on Spotify Web Player!")
# else:
#     print("No active Spotify devices found. Open the Web Player or Spotify app.")
# print(client_id,client_secret)


# def get_token():
#     auth_str = client_id+":"+client_secret
#     auth_bytes = auth_str.encode("utf-8")
#     auth_base64 = str(base64.b64encode(auth_bytes),"utf-8")
    
#     url = "https://accounts.spotify.com/api/token"
#     headers = {
#         "Authorization": "Basic " + auth_base64,
#         "Content-Type": "application/x-www-form-urlencoded"
#     }
    
#     data = {"grant_type": "client_credentials"}
    
#     result = post(url , headers=headers , data=data)
    
#     json_results = json.loads(result.content)
#     token = json_results["access_token"]
    
#     return token


# def get_auth_header(token):
#     return {"Authorization": "Bearer " + token}

# def search_Artist(token, artist_name):
#     url = "https://api.spotify.com/v1/search"
#     headers = get_auth_header(token)
#     query = f"?q={artist_name}&type=artist&limit=1"
    
#     query_url = url + query
#     result = get(query_url , headers=headers)
#     json_result = json.loads(result.content)["artists"]["items"]
    
#     if(len(json_result) == 0):
#         print("no artist with this name ...")
#         return None

#     return json_result[0]

# def search_song_for_artist(token , artist_id):
#     url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=INDIA"
#     header = get_auth_header(token)
#     result = get(url , headers=header)
#     json_result = json.loads(result.content)["tracks"]
#     return json_result

# token = get_token()
# # print(token)
# result = search_Artist(token , "pritam")
# artist_id = result["id"]

# songs = search_song_for_artist(token , artist_id)
# for idx,song in enumerate(songs):
#     print(f"{idx+1}. {song['name']}")
# print(songs)



#  making song playb on my localhost server
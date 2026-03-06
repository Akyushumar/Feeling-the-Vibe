from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

genius_client_id = os.getenv("GENIUS_CLIENT_ID")
genius_client_secret = os.getenv("GENIUS_CLIENT_SECRET")

def get_spotify_token():
    auth_string = f"{spotify_client_id}:{spotify_client_secret}"
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded" 
    }
    
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_spotify_auth_header(token = None):
    if token is None:
        token = get_spotify_token()
    return {"Authorization": f"Bearer {token}"}

def search_for_artist(token, artist_name):
    url = f"https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit=1"
    headers = get_spotify_auth_header(token)
    
    response = get(url, headers=headers)
    
    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        return None

    items = response.json().get('artists', {}).get('items', [])
    
    if not items:
        print("No artist found for:", artist_name)
        return None
        
    return items[0]  # Return the first artist found

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US"
    headers = get_spotify_auth_header(token)
    
    response = get(url, headers=headers)
    
    return response.json() if response.status_code == 200 else None

def search_for_track(token, track_name):
    url = f"https://api.spotify.com/v1/search?q={track_name}&type=track&limit=1"
    headers = get_spotify_auth_header(token)
    
    response = get(url, headers=headers)
    
    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        return None

    items = response.json().get('tracks', {}).get('items', [])
    
    if not items:
        print("No track found for:", track_name)
        return None
        
    return {
        "track_id": items[0]['id'],
        "track_name": items[0]['name'],
        "artist_name": items[0]['artists'][0]['name']
        }  # Return the first track found with its ID, name, and artist

def get_audio_features(token, track_id):
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = get_spotify_auth_header(token)
    
    response = get(url, headers=headers)
    
    result = response.json() if response.status_code == 200 else None
    
    print(result)
    
    return result
    
    
    #return response.json() if response.status_code == 200 else None

token = get_spotify_token() # Get the Spotify token once and reuse it for subsequent API calls
result_1 = search_for_artist(token, "acdc") 
artist_name = result_1['name'] if result_1 else "Unknown Artist"
artist_id = result_1['id'] if result_1 else None
result_2 = get_songs_by_artist(token, artist_id) if artist_id else None
track_name_1 = result_2['tracks'][0]['name'] if result_2 and result_2['tracks'] else None
track_id_1 = result_2['tracks'][0]['id'] if result_2 and result_2['tracks'] else None
audio_features = get_audio_features(token, track_id_1) if track_id_1 else None
print (track_name_1, track_id_1)
print (audio_features)


track_2 = search_for_track(token, "Bohemian Rhapsody")
print(track_2)
track_id_2 = track_2['track_id'] if track_2 else None



"""print (f"Top songs for artist {artist_name} (ID: {artist_id}):")

for idx, song in enumerate(result_2['tracks'][:5]):
    print(f"{idx + 1}. {song['name']} - {song['id']}")
    
print("\nAudio features for the first track:")
if audio_features:
    for feature, value in audio_features.items():
        print(f"{feature}: {value}")"""
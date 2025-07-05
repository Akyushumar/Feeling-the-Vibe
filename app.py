from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = f"{client_id}:{client_secret}"
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

def get_auth_header():
    token = get_token()
    return {"Authorization": f"Bearer {token}"}

def search_for_artist(token, artist_name):
    url = f"https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit=1"
    headers = get_auth_header()
    headers["Authorization"] = f"Bearer {token}"
    
    response = get(url, headers=headers)
    json_result = json.loads(response.content)['artists']['items']
    
    if response.status_code != 200 or len(json_result) == 0:
        return None
    
    return json_result

token = get_token()
#print(f"Access Token: {token}")
result = search_for_artist(token, "Adele")
print(result)
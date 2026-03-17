#%pip install lyricsgenius
import lyricsgenius
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

genius = None

def get_genius_client():
    global genius
    if genius is None:
        # Try Streamlit secrets first, fall back to .env
        try:
            token = st.secrets["GENIUS_ACCESS_TOKEN"]
        except:
            token = os.getenv("GENIUS_ACCESS_TOKEN")
        
        if not token:
            return None
            
        genius = lyricsgenius.Genius(
            token,
            skip_non_songs=True,
            excluded_terms=["(Remix)", "(Live)"],
            remove_section_headers=True,
            timeout=10,
            retries=2,
            verbose=False
        )
    return genius

def get_lyrics(track_name, artist_name):
    client = get_genius_client()
    try:
        if artist_name:
            song = client.search_song(track_name, artist_name)
        else:
            song = client.search_song(track_name)
        
        if song and song.lyrics:
            return song.lyrics.strip()
        return None
    except Exception as e:
        print(f"Lyrics fetch failed: {e}")
        return None
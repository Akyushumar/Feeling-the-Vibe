#%pip install lyricsgenius
import lyricsgenius
import os
from dotenv import load_dotenv

load_dotenv()

genius = None

def get_genius_client():
    global genius
    if genius is None:
        genius = lyricsgenius.Genius(
            os.getenv("GENIUS_CLIENT_ACCESS_TOKEN"),
            skip_non_songs=True,
            excluded_terms=["(Remix)", "(Live)", "(Cover)"],
            remove_section_headers=True,
            timeout=10,
            retries=3 
        )
        genius.verbose = False
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
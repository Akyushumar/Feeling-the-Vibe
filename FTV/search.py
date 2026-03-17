import pandas as pd
#%pip install rapidfuzz
from rapidfuzz import fuzz, process
import streamlit as st

df = None

@st.cache_data
def load_dataset(path="data/dataset.parquet"):
    return pd.read_parquet(path)

def find_track_in_dataset(track_name, artist_name=None):
    data = load_dataset()
    
    # Stage 1: exact lowercase match (fast)
    name_lower = track_name.lower().strip()
    candidates = data[data['name_lower'] == name_lower]
    
    # Stage 2: if no exact match, fuzzy search
    if candidates.empty:
        all_names = data['name_lower'].tolist()
        results = process.extract(
            name_lower, 
            all_names, 
            scorer=fuzz.token_sort_ratio, 
            limit=10,
            score_cutoff=80
        )
        if not results:
            return None
        indices = [r[2] for r in results]
        candidates = data.iloc[indices]
    
    # Stage 3: filter by artist if provided
    if artist_name and not candidates.empty:
        artist_lower = artist_name.lower().strip()
        artist_filtered = candidates[
            candidates['artists'].str.lower().str.contains(artist_lower, na=False)
        ]
        if not artist_filtered.empty:
            candidates = artist_filtered
    
    # Return best match as dict
    return candidates.iloc[0].to_dict()
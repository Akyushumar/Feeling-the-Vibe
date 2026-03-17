import streamlit as st
from FTV.search import find_track_in_dataset
from FTV.lyrics import get_lyrics
from FTV.analyse import analyse_lyrics, build_emotion_profile
from FTV.visualise import make_radar_chart

st.set_page_config(page_title="Feeling the Vibe", page_icon="🎵", layout="centered")

st.title("🎵 Feeling the Vibe")
st.caption("Song emotion analyser — audio features + lyrics sentiment")

track_name = st.text_input("Song name", placeholder="e.g. Happy")
artist_name = st.text_input("Artist (optional but recommended)", placeholder="e.g. Pharrell Williams")

if st.button("Analyse", type="primary"):
    if not track_name:
        st.warning("Enter a song name.")
    else:
        with st.spinner("🔍 Searching dataset..."):
            track = find_track_in_dataset(track_name, artist_name or None)
        
        if not track:
            st.error("Song not found in dataset. Try a different name or artist.")
        else:
            with st.spinner("📝 Fetching lyrics..."):
                lyrics = get_lyrics(track_name, artist_name or None)
            
            with st.spinner("🧠 Analysing sentiment..."):
                sentiment = analyse_lyrics(lyrics)
            
            profile = build_emotion_profile(track, sentiment)
            
            st.subheader(f"{profile['track_name']} — {profile['artists']}")
            st.caption(f"Released: {profile['year']}")
            
            if profile['is_instrumental']:
                st.info("Instrumental track — lyrics sentiment not available.")
            elif not profile['has_lyrics']:
                st.warning("Lyrics not found — showing audio features only.")
            
            fig = make_radar_chart(profile)
            st.plotly_chart(fig, use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Valence", f"{profile['audio_features']['valence']:.2f}")
                st.metric("Energy", f"{profile['audio_features']['energy']:.2f}")
                st.metric("Danceability", f"{profile['audio_features']['danceability']:.2f}")
            with col2:
                st.metric("Acousticness", f"{profile['audio_features']['acousticness']:.2f}")
                if sentiment:
                    st.metric("Lyrics Sentiment", f"{sentiment['compound']:.2f}")
                    st.metric("Sentiment Label", sentiment['label'].capitalize())
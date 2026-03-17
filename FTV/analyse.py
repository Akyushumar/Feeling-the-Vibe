#%pip install vaderSentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = None

def get_analyzer():
    global analyzer
    if analyzer is None:
        analyzer = SentimentIntensityAnalyzer()
    return analyzer

def analyse_lyrics(lyrics):
    if not lyrics:
        return None
    
    scores = get_analyzer().polarity_scores(lyrics)
    
    return {
        "compound": scores['compound'],      # -1 to +1, overall sentiment
        "positive": scores['pos'],           # proportion positive
        "negative": scores['neg'],           # proportion negative
        "neutral": scores['neu'],            # proportion neutral
        "label": classify_sentiment(scores['compound'])
    }

def classify_sentiment(compound):
    if compound >= 0.05:
        return "positive"
    elif compound <= -0.05:
        return "negative"
    else:
        return "neutral"

import ast

def clean_artists(artists_str):
    try:
        artists_list = ast.literal_eval(artists_str)
        return ", ".join(artists_list)
    except:
        return artists_str

def build_emotion_profile(track_dict, lyrics_sentiment):
    profile = {
        "track_name": track_dict.get("name"),
        "artists": clean_artists(track_dict.get("artists")),
        "year": track_dict.get("year"),
        "audio_features": {
            "valence": track_dict.get("valence"),
            "energy": track_dict.get("energy"),
            "danceability": track_dict.get("danceability"),
            "acousticness": track_dict.get("acousticness"),
            "tempo_normalised": min(track_dict.get("tempo", 0) / 200, 1.0)
        },
        "lyrics_sentiment": lyrics_sentiment,
        "has_lyrics": lyrics_sentiment is not None,
        "is_instrumental": track_dict.get("instrumentalness", 0) > 0.8
    }
    return profile
#%pip install plotly nbformat

import plotly.graph_objects as go

def make_radar_chart(profile):
    audio = profile["audio_features"]
    sentiment = profile["lyrics_sentiment"]
    
    categories = [
        "Valence", "Energy", "Danceability", 
        "Acousticness", "Tempo", "Lyrics Sentiment"
    ]
    
    # Normalise sentiment compound from [-1,1] to [0,1]
    sentiment_normalised = (sentiment["compound"] + 1) / 2 if sentiment else 0.5
    
    values = [
        audio["valence"],
        audio["energy"],
        audio["danceability"],
        audio["acousticness"],
        audio["tempo_normalised"],
        sentiment_normalised
    ]
    
    # Close the polygon
    values += values[:1]
    categories += categories[:1]
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(29, 185, 84, 0.2)',
        line=dict(color='#1DB954', width=2),
        name=profile["track_name"]
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1])
        ),
        showlegend=False,
        title=dict(
            text=f"{profile['track_name']} — {profile['artists']}",
            font=dict(size=16)
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig
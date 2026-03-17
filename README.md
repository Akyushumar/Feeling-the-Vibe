# Feeling the Vibe 🎵

**A hybrid song emotion analyser** that maps the emotional fingerprint of any song by combining Spotify audio features with real-time lyrics sentiment analysis. Search any song and get back a visual radar chart showing its emotional profile across six dimensions.

> Built to answer one question: *what does this song actually feel like?*

🔗 **[Live Demo](https://feeling-the-vibe-tmedmpx96pnxihue5zffig.streamlit.app/)**

---

## Features

| Feature | Description |
|---|---|
| **1.2M Song Dataset** | Pre-computed Spotify audio features from Kaggle — bypasses deprecated API |
| **Fuzzy Search** | Two-stage matching: exact → fuzzy with RapidFuzz across 1.2M tracks |
| **Lyrics Sentiment** | Real-time lyrics fetching via Genius API + VADER sentiment analysis |
| **Hybrid Emotion Profile** | Combines audio features + lyrics sentiment into one unified object |
| **Radar Chart** | Interactive Plotly chart across Valence, Energy, Danceability, Acousticness, Tempo, Lyrics Sentiment |
| **Graceful Degradation** | Instrumental tracks and missing lyrics handled cleanly — never hard-fails |
| **Streamlit Web UI** | Clean, dark-themed web interface with loading spinners and metric cards |

---

## Quick Start

### Prerequisites

- Python 3.10+
- A [Genius API](https://genius.com/api-clients) access token

### Setup

```bash
# Clone the repo
git clone https://github.com/Akyushumar/Feeling-the-Vibe.git
cd Feeling-the-Vibe

# Create virtual environment
python -m venv myenv
myenv\Scripts\activate    # Windows
# source myenv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### Dataset

Download the [Spotify Tracks Dataset](https://www.kaggle.com/datasets/maharshipandya/spotify-tracks-dataset) from Kaggle and place it at `data/dataset.csv`.

Then run the one-time conversion to Parquet:

```python
import pandas as pd

df = pd.read_csv('data/dataset.csv', usecols=[
    'id', 'name', 'artists', 'year',
    'danceability', 'energy', 'valence',
    'acousticness', 'tempo', 'loudness',
    'speechiness', 'instrumentalness'
])
df['name_lower'] = df['name'].str.lower().str.strip()
df.to_parquet('data/dataset.parquet', index=False)
```

### Environment Variables

Create a `.env` file in the project root:

```env
GENIUS_ACCESS_TOKEN=your_genius_access_token_here
```

Get your token from [genius.com/api-clients](https://genius.com/api-clients) → Create an API Client → copy the **Client Access Token**.

---

## Usage

```bash
streamlit run streamlit_app.py
```

Opens at **http://localhost:8501**

1. Enter a song name
2. Add the artist name (recommended for accuracy)
3. Click **Analyse**
4. Get the radar chart + sentiment breakdown

---

## Architecture

```
Feeling-the-Vibe/
├── streamlit_app.py        # Main Streamlit web interface
├── FTV/
│   ├── __init__.py
│   ├── search.py           # Fuzzy dataset lookup (RapidFuzz)
│   ├── lyrics.py           # Genius API lyrics fetching
│   ├── analyse.py          # VADER sentiment + emotion profile builder
│   └── visualise.py        # Plotly radar chart
├── data/
│   └── dataset.parquet     # 1.2M Spotify tracks (pre-computed features)
├── requirements.txt
└── .env                    # API keys (gitignored)
```

### How It Works

```
User inputs song name + artist
            │
            ▼
    Search dataset.parquet
    (exact match → fuzzy fallback)
            │
       ┌────┴────┐
       ▼         ▼
   Found      Not found
       │         │
       ▼         ▼
  Audio        Skip audio
  features     features
       │         │
       └────┬────┘
            ▼
   Fetch lyrics (Genius API)
            │
       ┌────┴────┐
       ▼         ▼
   Found      Not found /
       │      Instrumental
       ▼         │
  VADER         Skip sentiment
  sentiment      │
       │         │
       └────┬────┘
            ▼
   Build emotion profile
            │
            ▼
   Plotly radar chart
   + metric cards
```

---

## Benchmarks

*Benchmark suite in progress — 100 labelled songs across happy, sad, energetic, calm, and melancholic categories.*

**Validation examples:**

| Song | Artist | Valence | Energy | Sentiment | Label |
|---|---|---|---|---|---|
| Happy | Pharrell Williams | 0.96 | 0.76 | 0.9998 | Positive ✅ |
| Someone Like You | Adele | 0.18 | 0.34 | -0.42 | Negative ✅ |
| Cold Water | Major Lazer, Justin Bieber | 0.50 | 0.80 | 0.84 | Positive ✅ |

*Full benchmark results will be published in v1.1.*

---

## Tech Stack

| Component | Technology |
|---|---|
| Audio Features | Kaggle Spotify Tracks Dataset (1.2M tracks) |
| Song Matching | pandas + RapidFuzz (two-stage exact → fuzzy) |
| Lyrics | Genius API via lyricsgenius |
| Sentiment Analysis | VADER (vaderSentiment) |
| Visualisation | Plotly (interactive radar chart) |
| Web UI | Streamlit |
| Deployment | Streamlit Cloud |

---

## Known Limitations

| Limitation | Detail |
|---|---|
| **Spotify API deprecated** | `/audio-features` endpoint restricted for apps created after Nov 2024. This project uses a pre-built Kaggle dataset as a workaround. |
| **Dataset coverage** | 1.2M tracks covers most mainstream music but some songs may not be found, especially regional or very new releases. |
| **VADER + non-English lyrics** | VADER is optimised for English. Hindi, Korean, and other non-English lyrics will score near neutral unless they contain English words. Hinglish (Hindi-English mix) works reasonably well. |
| **Genius API rate limits** | Free tier has rate limits. Lyrics fetch may occasionally time out on the hosted demo. |

---

## Roadmap

- [ ] Benchmark suite — 100 labelled songs with accuracy metric
- [ ] Language detection — skip sentiment for non-English lyrics gracefully
- [ ] Compare mode — analyse two songs side by side
- [ ] Spotify OAuth — analyse your own listening history
- [ ] Mood clustering — KMeans on audio features to group songs by emotion

---

## License

MIT

---

*Part of a larger personal Spotify analytics project. Built with Python, curiosity, and too many late nights.*
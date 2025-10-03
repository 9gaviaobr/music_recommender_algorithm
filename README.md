## Collect · AI Music Recommender

A small, fully transparent content‑based music recommender. The system exposes a tiny HTTP API using Python’s standard library and a minimal frontend (HTML/CSS/JS) to explore recommendations by either seeding a track or setting preference sliders.

> [!NOTE]
> This project is designed for educational use: easy to read, easy to run, and easy to explain in an academic context.

---

### Key Features

- **Content-based recommendations** using cosine similarity
- **Two modes**: by seed track or by user preference vector
- **Zero dependencies** on the backend (Python stdlib HTTP server)
- **Tiny curated dataset** for clarity and reproducibility
- **No build step** on the frontend (pure HTML/CSS/JS)

---

### Tech Stack

- **Backend**: Python (stdlib `http.server`)
- **Frontend**: HTML, CSS, vanilla JavaScript
- **Data**: In-repo sample dataset (`backend/data.py`)

---

### Project Structure

- `backend/`
  - `server.py`: Minimal HTTP server that serves the frontend and exposes the API (`/api/tracks`, `/api/recommend`)
  - `recommender.py`: Cosine similarity, preference vector construction, top‑K retrieval
  - `data.py`: Small curated dataset and feature extraction
- `frontend/`
  - `index.html`: UI to select a seed track or tune preferences
  - `app.js`: Fetches data, calls the API, renders recommendations
  - `styles.css`: Basic styling

---

### Quickstart

- Prerequisites: Python 3.8+ (tested with standard library only)
- OS: Works on Windows/macOS/Linux. Example commands below use Windows PowerShell.

1) From the project root:
```
in powershell
py backend/server.py
      OR
in terminal
python -m backend.server
```

2) Open the app:
- `http://127.0.0.1:8000`

3) Interact:
- Click “Recommend similar” on any track to get seed‑based recommendations.
- Or adjust “Danceability”, “Energy”, “Valence”, and “Tempo” sliders, then click “Recommend from preferences”.

To stop the server: Ctrl+C in the terminal.

---

### API Reference

Base URL: `http://127.0.0.1:8000`

- **GET** `/api/tracks`
  - Returns the catalog.
  - Response:
    ```json
    {
      "tracks": [
        { "id": "t001", "title": "...", "artist": "...", "genre": "...", "year": 2021, "danceability": 0.78, "energy": 0.72, "valence": 0.65, "tempo_bpm": 118 }
        // ...
      ]
    }
    ```

- **GET** `/api/recommend`
  - Two modes:
    - Seed track mode: `?seed=<track_id>&k=<int>`
    - Preference mode: `?danceability=<0..1>&energy=<0..1>&valence=<0..1>&tempo=<0..1>&k=<int>`
  - Parameters:
    - `seed` (optional): track ID from `/api/tracks`
    - `danceability`, `energy`, `valence`, `tempo` (optional floats 0..1). Missing values default to 0.5
    - `k` (optional int): number of results (default 5)
  - Response:
    ```json
    {
      "recommendations": [
        { "id": "t005", "title": "...", "artist": "...", "genre": "...", "year": 2022, "danceability": 0.90, "energy": 0.77, "valence": 0.62, "tempo_bpm": 124 }
        // ...
      ]
    }
    ```

Example calls:
```bash
# Seed-based
curl "http://127.0.0.1:8000/api/recommend?seed=t001&k=5"

# Preference-based
curl "http://127.0.0.1:8000/api/recommend?danceability=0.7&energy=0.6&valence=0.8&tempo=0.5&k=5"
```

---

### How It Works (Methodology)

Each track is represented by a feature vector:
- `danceability` (0..1)
- `energy` (0..1)
- `valence` (0..1)
- `tempo` (scaled 0..1 from BPM assuming 60–160 BPM)

For preference mode, a user vector is constructed with defaults of 0.5 for any missing dimensions. For seed mode, we extract the feature vector of the chosen track. We then compute cosine similarity between the query vector and every track vector and return the top‑K by similarity.

Cosine similarity:
\[
\text{cosine}(a, b) = \frac{\sum_i a_i b_i}{\sqrt{\sum_i a_i^2}\sqrt{\sum_i b_i^2}}
\]

---

### Dataset

Found in `backend/data.py`. It’s intentionally small and balanced across a few genres and moods to keep the example transparent and readable. Tempo is normalized to 0..1 by a simple min‑max scaling over an assumed 60–160 BPM range.

---

### Reproducibility

- No randomness in the model; results are deterministic given the dataset and parameters.
- The entire pipeline is in this repo; no external services, databases, or model files.

---

### Limitations

- Small toy dataset; results demonstrate mechanism, not production quality.
- Content features are hand‑crafted and minimal; no learned embeddings.
- No user history, no collaborative filtering, no personalization beyond the input vector.

---

### Ethical Considerations

- Transparent by design (no opaque models).
- Extend responsibly if integrating user data; consider privacy, consent, and bias amplification.

---

### Future Expandability

- Add more features (e.g., acousticness, instrumentalness, loudness).
- Swap in learned embeddings (e.g., from audio or metadata encoders).
- Hybrid recommenders (content + collaborative signals).
- Pagination and filtering (genre/year constraints).
- Persisted user profiles and A/B experiments.
- Evaluation with larger datasets and offline metrics (MAP@K, NDCG).

---

### License

This project is licensed under the MIT License.  
Can only be used for educational and research purposes.

---

### Acknowledgements

Built with Python stdlib and a minimal web frontend to keep the focus on recommendation fundamentals.

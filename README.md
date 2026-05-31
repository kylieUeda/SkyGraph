# TravelTracker

A personal flight tracking web app that lets you log your travel history by uploading boarding pass photos. Flights are displayed as lines on an interactive world map.

## Features

- **Boarding pass OCR** — upload a photo of your boarding pass; the app extracts IATA airport codes automatically using EasyOCR
- **Interactive map** — flights are plotted as lines between departure and destination airports on a Leaflet.js world map
- **Persistent history** — every flight is saved to `flights_hist.csv` with airport names, coordinates, and timestamps
- **Manual entry** — a manual input option is available as an alternative to image upload

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML / CSS / Leaflet.js |
| Backend | Python / FastAPI |
| OCR | EasyOCR |
| Map tiles | CartoDB (via CDN) |
| Data | CSV (airport database + flight history) |

## Project Structure

```
FlightTracker/
├── main.py              # FastAPI server — /extract endpoint and CSV persistence
├── ocr.py               # OCR logic — extracts IATA codes from boarding pass images
├── index.html           # Frontend — map UI and file upload
├── style.css            # Styles
├── flights_hist.csv     # Your saved flight history
├── airports_iata.csv    # Airport database (IATA codes, names, coordinates)
├── airports.csv         # Extended airport data
├── regions.csv          # Region reference data
└── requirement.txt      # Python dependencies
```

## Setup

### Prerequisites

- Python 3.9+

### Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirement.txt
```

### Run the backend

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

### Open the frontend

Open `index.html` in your browser directly (no build step required).

## Usage

1. Click **+ Add New Flight** in the header.
2. Choose **Upload Image** and select a photo of your boarding pass (PNG or JPG).
3. The app reads the IATA airport codes via OCR, looks up the airport coordinates, draws a line on the map, and saves the flight to `flights_hist.csv`.

## API

### `POST /extract`

Accepts a boarding pass image, extracts the departure and destination IATA codes, and returns airport info.

**Request:** `multipart/form-data` with a `file` field (PNG or JPG).

**Response:**
```json
{
  "departure":    { "iata_code": "HNL", "name": "Daniel K. Inouye International Airport", "latitude": 21.318, "longitude": -157.925 },
  "destination":  { "iata_code": "JFK", "name": "John F. Kennedy International Airport",  "latitude": 40.639, "longitude": -73.779 }
}
```

### `GET /health`

Returns `{ "status": "ok" }`.

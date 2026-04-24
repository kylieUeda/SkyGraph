from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil, uuid, os, csv
from datetime import datetime
from ocr import extract_flight_info, get_airport_info

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
DATA_FILE = "flights_hist.csv" # file to save
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_to_csv(dep_info, dest_info):
    file_exists = os.path.isfile(DATA_FILE)
    with open(DATA_FILE, "a", newline="", encoding="utf-8") as f
        writer = csv.writer(f)
        # if file is new write a header
        if not file_exists:
            writer.writerow(["date", "dep_code", "dep_name", "dep_lat", "dep_lon", "dest_code", "dest_name", "dest_lat", "dest_lon"])
        # write data
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            dep_info["iata_code"], dep_info["name"], dep_info["latitude"], dep_info["longitude"],
            dest_info["iata_code"], dest_info["name"], dest_info["latitude"], dest_info["longitude"]
        ])

@app.post("/extract")
async def extract(file: UploadFile = File(...)):
    # format
    if not file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        raise HTTPException(400, "PNG or JPG only.")

    # temporal save
    tmp_path = f"{UPLOAD_DIR}/{uuid.uuid4()}_{file.filename}"
    with open(tmp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        pairs = extract_flight_info(tmp_path)
    except ValueError as e:
        raise HTTPException(422, str(e))
    finally:
        os.remove(tmp_path)

    # Get airport info
    dep_info = get_airport_info(pairs[0][0])
    dest_info = get_airport_info(pairs[0][1])

    # Save to CSV file
    save_to_csv(dep_info, dest_info)

    return {
        "departure": dep_info,
        "destination": dest_info,
    }

@app.get("/health")
def health():
    return {"status": "ok"}
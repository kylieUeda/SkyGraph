from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil, uuid, os
from ocr import extract_flight_info, get_airport_info

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/extract")
async def extract(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        raise HTTPException(400, "PNG or JPG only.")

    tmp_path = f"{UPLOAD_DIR}/{uuid.uuid4()}_{file.filename}"
    with open(tmp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        pairs = extract_flight_info(tmp_path)
    except ValueError as e:
        raise HTTPException(422, str(e))
    finally:
        os.remove(tmp_path)

    dep_code, dest_code = pairs[0]
    return {
        "departure": get_airport_info(dep_code),
        "destination": get_airport_info(dest_code),
    }

@app.get("/health")
def health():
    return {"status": "ok"}
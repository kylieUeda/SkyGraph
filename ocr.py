import easyocr
import re
import pandas as pd

iata_df = pd.read_csv("airports_iata.csv")
IATA = set(iata_df["iata_code"].dropna().str.upper())

# Read info from the image
def extract_flight_info(image_path):
    # initialize an OCR engine
    reader = easyocr.Reader(['en'])
    
    # read texts from an image
    results = reader.readtext(image_path, detail=0)
    
    full_text = " ".join(results).upper()

    # Read an airport code
    codes_set = re.findall(r'\b([A-Z]{3})\s+([A-Z]{3})\b', full_text)

    valid_sets = [
        (dep, dest)
        for dep, dest in codes_set
        if dep in IATA and dest in IATA
    ]
    
    # remove duplicate
    u_codes = list(set(valid_sets))

    return u_codes

# Get other info from the dataset
def get_airport_info(code):
    r = iata_df[iata_df["iata_code"] == code]

    return {
        "iata_code" : code,
        "name" : r["name"],
        "latitude" : r["latitude_deg"],
        "longitude" : r["longitude_deg"]
    }

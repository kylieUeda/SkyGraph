import easyocr
import re
import pandas as pd

# import cv2
# import os

# file_name = 'ticket_test.png'

# # 1. check if the image file is existing
# if os.path.exists(file_name):
#     print(f"Found {file_name}!")
    
#     # 2. Check if it is readable
#     img = cv2.imread(file_name)
#     if img is not None:
#         print(f"Successfully read the image file. size: {img.shape}")
#     else:
#         print("Error: Found the file, but couldn't read it.")
# else:
#     print(f"Error: No file named '{file_name}' found.")


def extract_flight_info(image_path):
    # initialize an OCR engine (jpn & en)
    reader = easyocr.Reader(['en'])
    
    # read texts from an image
    results = reader.readtext(image_path, detail=0)
    full_text = " ".join(results).upper()
    
    print(f"--- Text ---\n{full_text}\n------------------")

    # Read an airport code
    airport_codes = re.findall(r'\b([A-Z]{3})\s+([A-Z]{3})\b', full_text)

    
    # remove duplicate
    u_codes = list(set(airport_codes))
    # print("airport codes: ", u_codes)
    return u_codes

# test
codes = extract_flight_info('ticket_test.png')

iata = pd.read_csv("airports_iata.csv")

# Get IATA code for departure and arrival airport
dep_code = codes[0][0]
dest_code = codes[0][1]

# Get info about depature and arrival airport
dep_row = iata[iata["iata_code"] == dep_code]
dest_row = iata[iata["iata_code"] == dest_code]

print(f'The flight departed at {dep_row["name"].item()} and arrived at {dest_row["name"].item()}!')
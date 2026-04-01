import easyocr
import re

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
    reader = easyocr.Reader(['en', 'ja'])
    
    # read texts from an image
    results = reader.readtext(image_path, detail=0)
    full_text = " ".join(results).upper()
    
    print(f"--- Text ---\n{full_text}\n------------------")

    # Read an airport code
    airport_codes = re.findall(r'\b[A-Z]{3}\b', full_text)
    
    # remove duplicate
    unique_codes = list(set(airport_codes))
    return unique_codes

# test
codes = extract_flight_info('ticket_test.png')
print(f"airport codes: {codes}")
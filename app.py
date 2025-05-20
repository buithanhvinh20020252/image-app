import eel
import cv2
import base64
import numpy as np

from otsu_threshold import otsu_threshold
from adaptive_mean_threshold import adaptive_mean_threshold, fast_adaptive_mean_threshold

eel.init('web')

def base64_to_cv2(image_data):
    header, encoded = image_data.split(',', 1)  # Split out the metadata from the base64 data
    img_data = base64.b64decode(encoded)  # Decode the base64 string
    img_array = np.frombuffer(img_data, dtype=np.uint8)  # Convert to a NumPy array
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  # Decode to OpenCV image
    return img

# Function to convert OpenCV image (NumPy array) to base64-encoded image data
def cv2_to_base64(cv_image):
    _, buffer = cv2.imencode('.png', cv_image)  # Encode image to PNG
    b64_result = base64.b64encode(buffer).decode('utf-8')  # Convert to base64 string
    return f"data:image/png;base64,{b64_result}"

@eel.expose
def grayscale_image(image_data):

    cv2_image = base64_to_cv2(image_data)

    grayscale = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2GRAY)

    result_b64 = cv2_to_base64(grayscale)

    # Placeholder: simply return the original image
    return result_b64

@eel.expose
def process_threshold(image_data, threshold):
    img = base64_to_cv2(image_data)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, segmented = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

    result_b64 = cv2_to_base64(segmented)
    
    return result_b64


@eel.expose
def process_otsu_threshold(image_data):
    img = base64_to_cv2(image_data)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   
    #lib_threshold, segmented = lib_otsu_threshold(gray)
    threshold, segmented = otsu_threshold(gray)

    result_b64 = cv2_to_base64(segmented)

    return result_b64, int(threshold)

@eel.expose 
def process_adaptive_mean_threshold(image_data):
    img = base64_to_cv2(image_data)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   
    #lib_threshold, segmented = lib_otsu_threshold(gray)
    segmented = fast_adaptive_mean_threshold(gray)

    result_b64 = cv2_to_base64(segmented)

    return result_b64

def lib_adaptive_mean_threshold(image):
    return cv2.adaptiveThreshold(image ,255, cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)

def lib_otsu_threshold(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

port = 8000

print(f"Your app is hosted on port {port}")

eel.start('index.html', mode=None, port=port)

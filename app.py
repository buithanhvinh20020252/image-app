import eel
import cv2
import base64
import numpy as np
import os

from otsu_threshold import otsu_threshold
from adaptive_mean_threshold import fast_adaptive_mean_threshold

eel.init('web')

def base64_to_cv2(image_data):
    header, encoded = image_data.split(',', 1)
    img_data = base64.b64decode(encoded)
    img_array = np.frombuffer(img_data, dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

def cv2_to_base64(cv_image):
    _, buffer = cv2.imencode('.png', cv_image)
    b64_result = base64.b64encode(buffer).decode('utf-8')
    return f"data:image/png;base64,{b64_result}"

def find_and_save_objects(binary_image, original_image, output_folder="objects"):
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    result = original_image.copy()
    count = 0

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        if area > 100:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)
            obj = original_image[y:y + h, x:x + w]
            cv2.imwrite(os.path.join(output_folder, f"object_{i + 1}.png"), obj)
            count += 1

    return result, count

@eel.expose
def grayscale_image(image_data):
    cv2_image = base64_to_cv2(image_data)
    grayscale = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2GRAY)
    return cv2_to_base64(grayscale)

@eel.expose
def process_threshold_with_boxes(image_data, threshold):
    img = base64_to_cv2(image_data)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    boxed_img, count = find_and_save_objects(binary, img)
    return {
        "binary": cv2_to_base64(binary),
        "boxed": cv2_to_base64(boxed_img),
        "count": count
    }

@eel.expose
def process_otsu_with_boxes(image_data):
    img = base64_to_cv2(image_data)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    threshold, binary = otsu_threshold(gray)
    boxed_img, count = find_and_save_objects(binary, img)
    return {
        "threshold": int(threshold),
        "binary": cv2_to_base64(binary),
        "boxed": cv2_to_base64(boxed_img),
        "count": count
    }

@eel.expose
def process_adaptive_mean_with_boxes(image_data):
    img = base64_to_cv2(image_data)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    binary = fast_adaptive_mean_threshold(gray)
    boxed_img, count = find_and_save_objects(binary, img)
    return {
        "binary": cv2_to_base64(binary),
        "boxed": cv2_to_base64(boxed_img),
        "count": count
    }

eel.start('index.html', port=7999)

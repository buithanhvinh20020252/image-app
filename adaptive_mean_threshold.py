import numpy as np
import cv2

def adaptive_mean_threshold(gray_img, block_size=11, C=2):
    height, width = gray_img.shape
    pad = block_size // 2
    padded_img = cv2.copyMakeBorder(gray_img, pad, pad, pad, pad, cv2.BORDER_REFLECT)
    result = np.zeros_like(gray_img, dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            y1, y2 = y, y + block_size
            x1, x2 = x, x + block_size
            block = padded_img[y1:y2, x1:x2]
            local_mean = np.mean(block)
            threshold = local_mean - C
            result[y, x] = 255 if gray_img[y, x] > threshold else 0

    return result

def fast_adaptive_mean_threshold(gray, block_size=11, C=2):
    pad = block_size // 2
    h, w = gray.shape
    integral = cv2.integral(gray, sdepth=cv2.CV_64F)
    out = np.zeros_like(gray, dtype=np.uint8)

    y, x = np.ogrid[0:h, 0:w]
    x1 = np.clip(x - pad, 0, w)
    x2 = np.clip(x + pad + 1, 0, w)
    y1 = np.clip(y - pad, 0, h)
    y2 = np.clip(y + pad + 1, 0, h)

    A = integral[y1, x1]
    B = integral[y1, x2]
    C_ = integral[y2, x1]
    D = integral[y2, x2]

    block_sum = D - B - C_ + A
    block_area = (y2 - y1) * (x2 - x1)
    block_mean = block_sum / block_area

    out[gray > (block_mean - C)] = 255
    return out

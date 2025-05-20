import numpy as np
import cv2

def adaptive_mean_threshold(gray_img, block_size=11, C=2):
    height, width = gray_img.shape
    
    # Pad image based on block size
    pad = block_size // 2
    padded_img = cv2.copyMakeBorder(gray_img, pad, pad, pad, pad, cv2.BORDER_REFLECT)

    # Output binary image
    result = np.zeros_like(gray_img, dtype=np.uint8)

    # Iterate through each pixel
    for y in range(height):
        for x in range(width):
            # Extract the local block
            y1, y2 = y, y + block_size
            x1, x2 = x, x + block_size
            block = padded_img[y1:y2, x1:x2]

            # Compute mean of block
            local_mean = np.mean(block)

            # Threshold for this pixel
            threshold = local_mean - C

            # Apply threshold
            result[y, x] = 255 if gray_img[y, x] > threshold else 0

    return result


def fast_adaptive_mean_threshold(gray, block_size=11, C=2):
    pad = block_size // 2
    h, w = gray.shape

    # Compute the integral image (OpenCV returns float64 by default)
    integral = cv2.integral(gray, sdepth=cv2.CV_64F)

    # Create output image
    out = np.zeros_like(gray, dtype=np.uint8)

    # Define coordinates for top-left and bottom-right of each block
    y, x = np.ogrid[0:h, 0:w]

    x1 = np.clip(x - pad, 0, w)
    x2 = np.clip(x + pad + 1, 0, w)
    y1 = np.clip(y - pad, 0, h)
    y2 = np.clip(y + pad + 1, 0, h)

    # Get the four corner values from the integral image
    A = integral[y1, x1]
    B = integral[y1, x2]
    C_ = integral[y2, x1]
    D = integral[y2, x2]

    # Compute block sums and means
    block_sum = D - B - C_ + A
    block_area = (y2 - y1) * (x2 - x1)
    block_mean = block_sum / block_area

    # Apply threshold
    out[gray > (block_mean - C)] = 255

    return out
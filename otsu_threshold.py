import numpy as np
import cv2

def otsu_threshold(gray_img):
    # Histogram 
    hist, _ = np.histogram(gray_img.ravel(), bins=256, range=(0, 256))
    hist = hist.astype(np.float64)

    # Normalized histogram 
    hist_nomarlized = hist / hist.sum()

    bins = np.arange(256)

    # P1(k)
    p_1 = np.cumsum(hist_nomarlized)                         

    # m(k)
    m_k = np.cumsum(bins * hist_nomarlized)       

    # mG
    m_G = m_k[-1]                                           

    numerator = (m_G * p_1 - m_k) ** 2
    denominator = p_1 * (1 - p_1)

    with np.errstate(divide='ignore', invalid='ignore'):
        between_class_variances = np.where(denominator > 0, numerator / denominator, 0) # Sigmas

    best_threshold = np.argmax(between_class_variances)

    _, segmented = cv2.threshold(gray_img, best_threshold, 255, cv2.THRESH_BINARY)

    return best_threshold, segmented
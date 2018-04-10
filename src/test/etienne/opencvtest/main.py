import cv2
import numpy as np
import matplotlib.pyplot as plt

# Query image
img1 = cv2.imread("C:\\Users\\Admin\\Pictures\\opencv\\image2.png", 1)

# Train image
img2 = cv2.imread("C:\\Users\\Admin\\Pictures\\opencv\\image6.png", 1)

# Initiate ORB detector
orb = cv2.ORB_create()

# Find the keypoints and descriptors with SIFT
kp1, dest1 = orb.detectAndCompute(img1, None)
kp2, dest2 = orb.detectAndCompute(img2, None)

# Create BFMatcher object
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)

# Match descriptors
matches = bf.match(dest1, dest2)

# Sort them in the order of their distance
matches = sorted(matches, key = lambda x:x.distance)

# Draw first 10 matches
img3 = cv2.drawMatches(img1, kp1, img2, kp2, matches[:10], None, flags=2)

plt.imshow(img3)
plt.show()









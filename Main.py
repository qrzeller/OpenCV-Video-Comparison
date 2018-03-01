import cv2
import numpy as np

# http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_matcher/py_matcher.html#matcher

# cv2.NORM_L1
from matplotlib import pyplot

crosscheck = False
matcher = cv2.BFMatcher(cv2.NORM_L2, crosscheck )


#img1 = cv2.imread('Nemo-FN.png')
#img2 = cv2.imread('Nemo_Promo_5.jpg')

img1 = cv2.imread('special-k1.jpg')
img2 = cv2.imread('special-k2.jpg')
gray1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)

sift = cv2.xfeatures2d.SIFT_create()


kp1, des1 = sift.detectAndCompute(gray1,None)
kp2, des2 = sift.detectAndCompute(gray2,None)


#  matches = matcher.match(des1,des2)
matches = matcher.knnMatch(des1,des2, k=2)

# k best matches
# matcher.knnMatch()
# cv2.drawMatchesKnn

# Sort them in the order of their distance.
#matches = sorted(matches, key = lambda x:x.distance)



good = []
for m,n in matches:
    if m.distance < 0.75*n.distance:
        good.append([m])

print(len(good))

img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,None, flags=2)

##img=cv2.drawKeypoints(gray,kp,img)






pyplot.imshow(img3),pyplot.show()
#cv2.imwrite('sift_keypoints.jpg',img)

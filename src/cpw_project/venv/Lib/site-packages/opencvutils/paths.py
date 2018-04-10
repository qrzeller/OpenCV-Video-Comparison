import os
import numpy as np
import cv2
# import sys
from .utils import python_ver


if python_ver()[0] == 2:
	from urllib import urlopen
else:
	from urllib.request import urlopen


def list_images(basePath, contains=None):
	# return the set of files that are valid
	return list_files(basePath, validExts=(".jpg", ".jpeg", ".png", ".bmp"), contains=contains)


def list_files(basePath, validExts=(".jpg", ".jpeg", ".png", ".bmp"), contains=None):
	# loop over the directory structure
	for (rootDir, dirNames, filenames) in os.walk(basePath):
		# loop over the filenames in the current directory
		for filename in filenames:
			# if the contains string is not none and the filename does not contain
			# the supplied string, then ignore the file
			if contains is not None and filename.find(contains) == -1:
				continue

			# determine the file extension of the current file
			ext = filename[filename.rfind("."):].lower()

			# check to see if the file is an image and should be processed
			if ext.endswith(validExts):
				# construct the path to the image and yield it
				imagePath = os.path.join(rootDir, filename).replace(" ", "\\ ")
				yield imagePath


def url_to_image(url, readFlag=cv2.IMREAD_COLOR):
	# download the image, convert it to a NumPy array, and then read
	# it into OpenCV format
	resp = urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, readFlag)

	# return the image
	return image

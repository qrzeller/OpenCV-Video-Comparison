from __future__ import print_function
import numpy as np
import cv2
# import glob
import yaml


class CameraCalibration(object):
	'''
	Simple calibration class.
	'''
	marker_checkerboard = True
	marker_size = None

	def __init__(self, show_markers=True):
		self.show_markers = show_markers

	def __del__(self):
		cv2.destroyAllWindows()

	# # write camera calibration file out
	def save(self, save_file):
		fd = open(save_file, "w")
		yaml.dump(self.data, fd)
		fd.close()
		# with open(self.save_file, 'w') as f:
		# 	json.dump(self.data, f)

	# read camera calibration file in
	def read(self, matrix_name):
		fd = open(matrix_name, "r")
		self.data = yaml.load(fd)
		fd.close()
		# with open(matrix_name, 'r') as f:
		# 	self.data = json.load(f)

	# print the estimated camera parameters
	def printMatrix(self):
		# self.data = {'camera_matrix': mtx, 'dist_coeff': dist, 'newcameramtx': newcameramtx}
		# print 'mtx:',self.data['camera_matrix']
		# print 'dist:',self.data['dist_coeff']
		# print 'newcameramtx:',self.data['newcameramtx']
		m = self.data['camera_matrix']
		k = self.data['dist_coeff']
		print('focal length {0:3.1f} {1:3.1f}'.format(m[0][0], m[1][1]))
		print('image center {0:3.1f} {1:3.1f}'.format(m[0][2], m[1][2]))
		print('radial distortion {0:3.3f} {1:3.3f}'.format(k[0][0], k[0][1]))
		print('tangental distortion {0:3.3f} {1:3.3f}'.format(k[0][2], k[0][3]))
		print('RMS error:', self.data['rms'])

	# Pass a gray scale image and find the markers (i.e., checkerboard, circles)
	def findMarkers(self, gray, objpoints, imgpoints):
		# objp = np.zeros((self.marker_size[0]*self.marker_size[1],3), np.float32)
		# objp[:,:2] = np.mgrid[0:self.marker_size[0],0:self.marker_size[1]].T.reshape(-1,2)
		objp = np.zeros((np.prod(self.marker_size), 3), np.float32)
		objp[:, :2] = np.indices(self.marker_size).T.reshape(-1, 2)  # make a grid of points

		# Find the chess board corners or circle centers
		if self.marker_checkerboard is True:
			ret, corners = cv2.findChessboardCorners(gray, self.marker_size)
		else:
			ret, corners = cv2.findCirclesGrid(gray, self.marker_size, flags=cv2.CALIB_CB_ASYMMETRIC_GRID)

		# If found, add object points, image points (after refining them)
		if ret:
			print('[+] found ', corners.size / 2, 'of', self.marker_size[0]*self.marker_size[1], 'corners')
			term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
			cv2.cornerSubPix(gray, corners, (5, 5), (-1, -1), term)
			imgpoints.append(corners.reshape(-1, 2))
			objpoints.append(objp)

			# Draw the corners
			self.draw(gray, corners)
		else:
			print('[-] Could not find markers')

		return ret, objpoints, imgpoints

	# draw the detected corners on the image for display
	def draw(self, image, corners):
		if not self.show_markers:
			return image
		# Draw and display the corners
		if corners is not None:
			cv2.drawChessboardCorners(image, self.marker_size, corners, True)
		cv2.imshow('camera', image)
		cv2.waitKey(500)
		return image

	# use a calibration matrix to undistort an image
	def undistort(self, image):
		# undistort
		dst = cv2.undistort(image, self.data['camera_matrix'], self.data['dist_coeff'], None, self.data['newcameramtx'])
		return dst

	# run the calibration process on a series of images
	def calibrate(self, images, alpha=0.5, marker_size=(9, 6)):
		"""
		images: an array of calibration images, all assumed to be the same size

		alpha = 0: returns undistored image with minimum unwanted pixels (image
					pixels at corners/edges could be missing)
		alpha = 1: retains all image pixels but there will be black to make up
					for warped image correction
		"""

		self.marker_size = marker_size

		# Arrays to store object points and image points from all the images.
		objpoints = []  # 3d point in real world space
		imgpoints = []  # 2d points in image plane.
		w, h = 0, 0

		for fname in images:
			gray = cv2.imread(fname, 0)
			_, objpoints, imgpoints = self.findMarkers(gray, objpoints, imgpoints)
			h, w = gray.shape[:2]
			# print(fname,h,w)

		# print len(objpoints),len(imgpoints),w,h

		rms, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, (w, h), None, None)

		# Adjust the calibrations matrix
		# alpha=0: returns undistored image with minimum unwanted pixels (image pixels at corners/edges could be missing)
		# alpha=1: retains all image pixels but there will be black to make up for warped image correction
		# returns new cal matrix and an ROI to crop out the black edges
		newcameramtx, _ = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), alpha)
		self.data = {'camera_matrix': mtx, 'dist_coeff': dist, 'newcameramtx': newcameramtx, 'rms': rms, 'rvecs': rvecs, 'tvecs': tvecs}
		return self.data

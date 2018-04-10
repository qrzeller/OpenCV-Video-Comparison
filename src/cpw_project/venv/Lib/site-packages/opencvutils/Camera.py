#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
import cv2             # OpenCV camera
import time            # sleep
import platform        # determine linux or darwin (OSX)
import os              # check for travis.ci environment


# travis-ci has a fit ... trying to get around it
if platform.system().lower() == 'linux' and 'TRAVIS' not in os.environ:
	import picamera
	import picamera.array
else:
	# from .fake_hw import picamera
	from fake_rpi import picamera


class VideoError(Exception):
	pass


class SaveVideo(object):
	"""
	Simple class to save frames to video (mp4v)

	macOS: avc1
	windows: h264?
	"""

	def __init__(self):
		self.out = None
		self.encoder('avc1')

	def open(self, filename, width, height, fps=30):
		self.out = cv2.VideoWriter()
		self.out.open(filename, self.mpg4, fps, (width,height))

	def encoder(self, fourcc):
		try:
			self.mpg4 = cv2.VideoWriter_fourcc(*fourcc)
		except Exception as err:
			print(err)
			print('Please select another encoder for your platform')
			raise

	def __del__(self):
		self.release()

	def write(self, image):
		self.out.write(image)

	def release(self):
		if self.out:
			self.out.release()


# class VideoPublisher(object):
# 	"""
# 	"""
# 	def __init__(self):
# 		pass


CAMERA_PI = 0
CAMERA_CV = 1
CAMERA_VIDEO = 2  # useful??

kind = {
	0: 'pi',
	1: 'cv',
	2: 'video'
}


class CameraPi(object):
	ctype = CAMERA_PI

	def __init__(self):
		self.camera = picamera.PiCamera()

	def __del__(self):
		# the red light should shut off
		self.close()

	def close(self):
		self.camera.close()
		print('exiting CameraPi ... bye!')

	def init(self, win, cameraNumber, fileName, calibration):
		# self.camera.vflip = True  # camera is mounted upside down
		self.camera.resolution = win
		self.bgr = picamera.array.PiRGBArray(self.camera, size=win)

		if calibration:
			self.cal = calibration

	def read(self):
		self.camera.capture(self.bgr, format='bgr', use_video_port=True)
		tmp = self.bgr.array
		img = tmp.copy()
		self.bgr.truncate(0)  # clear stream

		return True, img

	def isOpen(self):
		return True  # FIXME 2016-05-15

	def type(self):
		return self.ctype

	# def get(self, display=True):
	# 	if display:
	# 		print('-----------------')
	# 		print('Pi Camera')
	# 		print('-----------------')
	#
	# 	return {'type': 'PiCamera'}


class CameraCV(object):
	ctype = CAMERA_CV

	def __init__(self):
		self.camera = cv2.VideoCapture()

	def __del__(self):
		self.close()

	def close(self):
		self.camera.release()
		print('exiting CameraCV ... bye!')

	def init(self, win=None, cameraNumber=None, fileName=None, calibration=None):
		# print('win', win)
		if (cameraNumber or cameraNumber == 0) and not fileName:
			live = True
			port = cameraNumber
		elif fileName:
			live = False
			port = fileName
		else:
			raise VideoError('CameraCV::init() must set cameraNumber OR fileName')

		self.camera.open(port)
		time.sleep(1)  # let camera warm-up

		if live:
			# print('setting win size to:', win)
			self.camera.set(3, win[0])
			self.camera.set(4, win[1])

		if calibration:
			self.cal = calibration

	def read(self):
		ret, img = self.camera.read()
		if not ret:
			return False, None

		return True, img

	def isOpen(self):
		return self.camera.isOpened()

	def type(self):
		return self.ctype

	# def get(self, display=True):
	# 	if display:
	# 		print('-----------------')
	# 		print('OpenCV Camera')
	# 		print('-----------------')
	#
	# 	return {'type': 'OpenCV', 'number': 0, 'size': (0, 0)}


class Camera(object):
	"""
	Generic camera object that can switch between OpenCV in PiCamera. This can
	also handle reading mp4's using OpenCV too.
	"""
	camera = None
	gray = False

	def __init__(self, cam='cv'):
		"""
		Constructor
		Sets up the camera either for OpenCV camera or PiCamera. If nothing is
		passed in, then it determines the operating system and picks which
		camera to use.
		types:
			pi - PiCamera
			cv - an OpenCV camera
			video - an mjpeg video clip to read from
		default:
			linux: PiCamera
			OSX: OpenCV
		in: type: cv video, or pi
		out: None
		"""
		self.cal = None
		# sys = platform.system().lower()  # grab OS name and make lower case

		if cam == 'pi':
			self.camera = CameraPi()
		elif cam == 'cv' or cam == 'video':
			self.camera = CameraCV()
		else:
			raise VideoError('Error, {0!s} not supported'.format((cam)))

		# print('[+] Camera type {}'.format(self.camera.type()))

	def __del__(self):
		self.close()

	def close(self):
		self.camera.close()

	def init(self, win=(640, 480), cameraNumber=None, fileName=None, calibration=None):
		"""
		Initialize the camera and set the image size
		in: image size (tuple (width,height), cameraNumber, calibration)
		out: None
		"""
		self.camera.init(win=win, cameraNumber=cameraNumber, fileName=fileName, calibration=calibration)

	def read(self):
		"""
		Reads a gray scale image
		in: None
		out: cv image (numpy array) in grayscale
		"""
		ret, img = self.camera.read()

		if self.cal and ret:  # FIXME 2016-05-15
			print('do calibration correction ... not done yet')

		if self.gray and ret:
			img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		return ret, img

	def isOpen(self):
		"""
		Determines if the camera is opened or not
		in: None
		out: True/False
		"""
		return self.camera.isOpen()

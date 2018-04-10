import sys
import cv2


def python_ver():
	"""Returns a tuple with the python version"""
	return sys.version_info[:3]


def get_opencv_version():
	"""Returns a tuple with the OpenCV version in it"""
	return tuple(map(int, cv2.__version__.split('.')))


def is_cv2():
	# if we are using OpenCV 2.x, then our cv2.__version__ will start
	# with 2.
	return True if get_opencv_version()[0] == 2 else False


def is_cv3():
	# if we are using OpenCV 3.X, then our cv2.__version__ will start
	# with 3.
	return True if get_opencv_version()[0] == 3 else False

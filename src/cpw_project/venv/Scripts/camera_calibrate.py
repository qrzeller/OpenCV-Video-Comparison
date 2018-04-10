#!C:\Users\Admin\PycharmProjects\cpw_project\venv\Scripts\python.exe
# --------------------------------------------------------------------
# Kevin J. Walchko
# 4 May 2014
#
# To do:
# - command line args is still shoddy
# x pass image list from command line
# x pass checkerboard or circles from command line
# x pass save file name from command line
# - remove getOptimalNewCameraMatrix()? not sure of its value
# --------------------------------------------------------------------

# A good resource:
# http://docs.opencv.org/3.1.0/dc/dbb/tutorial_py_calibration.html

from __future__ import print_function
from opencvutils import CameraCalibration
# import numpy as np
import cv2
import glob
# import yaml
import argparse
from opencvutils import __version__ as VERSION


# set up and handle command line args
def handleArgs():
	parser = argparse.ArgumentParser(version=VERSION, description='A simple program to calibrate a camera')
	parser.add_argument('-m', '--matrix', help='save calibration values', default='calibration.npy')
	parser.add_argument('-t', '--target', help='target type: chessboard or circles', default='chessboard')
	parser.add_argument('-s', '--target_size', type=int, nargs=2, help='size of pattern, for example, (6,7)', default=(11, 4))
	parser.add_argument('-p', '--path', help='location of images to use', required=True)
	parser.add_argument('-d', '--display', help='display images', default=True)

	args = vars(parser.parse_args())
	return args


# main function
def main():
	args = handleArgs()
	imgs_folder = args['path']

	print('Searching {0!s} for images'.format(imgs_folder))

	# calibration_images = '%s/left*.jpg' % (imgs_folder)
	calibration_images = '{0!s}/shot_*.png'.format((imgs_folder))
	images = []
	images = glob.glob(calibration_images)

	print('Number images found: {0:d}'.format(len(images)))
	# print(images)

	cal = CameraCalibration()
	cal.save_file = args['matrix']
	cal.marker_size = (args['target_size'][0], args['target_size'][1])

	print('Marker size:', cal.marker_size)

	if args['target'] == 'chessboard':
		cal.marker_checkerboard = True
	else:
		cal.marker_checkerboard = False
	cal.calibrate(images)

	cal.printMat()

	# save data to file
	cal.save('calibration.npy')

	# -----------------------------------------------------------------

	# read back in
	cal.read('calibration.npy')

	# crop the image
	# x,y,w,h = roi
	# crop the distorted edges off
	# # dst = dst[y:y+h, x:x+w]
	# cv2.imwrite('calibresult.png',dst)

	image = cv2.imread(images[0], 0)
	dst = cal.undistort(image)
	cv2.imshow('calibrated image', dst)
	# cv2.imshow('original image', image)
	cv2.waitKey(0)

	cv2.destroyAllWindows()


if __name__ == "__main__":
	main()

#!C:\Users\Admin\PycharmProjects\cpw_project\venv\Scripts\python.exe
#
# Author: Kevin J. Walchko
# Date: 11 May 2014
# Version: 0.3
# -------------------------------
#
#
#
from __future__ import print_function
import cv2
import yaml
import argparse
from opencvutils import Camera
from opencvutils import SaveVideo
from opencvutils import __version__ as VERSION
from time import sleep


def read(matrix_name):
	"""
	read camera calibration file in
	"""
	fd = open(matrix_name, "r")
	data = yaml.load(fd)
	return data


if __name__ == '__main__':

	parser = argparse.ArgumentParser(version=VERSION, description='A simple \
	program to capture images from a camera.You can capture a single frame \
	using the "f" or a video by using "v"')

	parser.add_argument('-c', '--camera', help='which camera to use, default is 0', default=0)
	parser.add_argument('-p', '--path', help='location to grab images, default is current directory', default='.')
	parser.add_argument('-f', '--video_filename', help='video file name, default is "out.mp4"', default='out')
	parser.add_argument('-n', '--numpy', type=str, help='numpy camera calibration matrix')
	parser.add_argument('-s', '--size', type=int, nargs=2, help='size of image capture, i.e., 640 480')

	args = vars(parser.parse_args())

	source = args['camera']
	shotdir = args['path']
	filename = args['video_filename']

	# image size
	if args['size'] is not None:
		size = (args['size'][0], args['size'][1])
		print('camera capturing images at size: {}'.format(size))
	else:
		size = (640, 480)

	# calibration matrix
	if args['numpy'] is not None:
		cam_cal = args['numpy']
		d = read(cam_cal)
		m = d['camera_matrix']
		k = d['dist_coeff']
		print('Using supplied camera calibration matrix: {}'.format(cam_cal))

	# print size
	# print cam_cal

	save = SaveVideo()

	# open camera
	cap = Camera()
	cap.init(win=size, cameraNumber=source)

	print('---------------------------------')
	print(' ESC/q to quit')
	print(' v to start/stop video capture')
	print(' f to grab a frame')
	print('---------------------------------')

	shot_idx = 0
	video_idx = 0
	video = False
	vfn = None
	FPS = 30
	sleep_time = 1.0/float(FPS)  # 30 FPS

	# Main loop ---------------------------------------------
	while True:
		ret, img = cap.read()

		if args['numpy'] is not None:
			img = cv2.undistort(img, m, k)

		cv2.imshow('capture', img)
		ch = cv2.waitKey(20)

		# Quit program using ESC or q
		if ch in [27, ord('q')]:
			if video:
				save.release()
			exit(0)

		# Start/Stop capturing video
		elif ch == ord('v'):
			if video is False:
				# setup video output
				vfn = '{0!s}_{1:d}.mp4'.format(filename, video_idx)
				h, w = img.shape[:2]
				save.start(vfn, (w, h), FPS)
				print('[+] start capture', vfn)
			else:
				save.release()
				video_idx += 1
				print('[-] stop capture', vfn)
			video = not video

		# Capture a single frame
		elif ch == ord('f'):
			fn = '{0!s}/shot_{1:03d}.png'.format(shotdir, shot_idx)
			cv2.imwrite(fn, img)
			print('[*] saved image to', fn)
			shot_idx += 1

		if video:
			save.write(img)
			sleep(sleep_time)

	cv2.destroyAllWindows()

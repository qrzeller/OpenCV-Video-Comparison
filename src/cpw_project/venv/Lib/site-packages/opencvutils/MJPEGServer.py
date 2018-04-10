from __future__ import print_function
from __future__ import division
import cv2
import time
from .opencvutils import Camera
import socket as Socket

from opencvutils import python_ver

if python_ver()[0] == 3:
	from http.server import BaseHTTPRequestHandler
else:
	from BaseHTTPServer import BaseHTTPRequestHandler


# import errno

# threaded version
# http://stackoverflow.com/questions/12650238/processing-simultaneous-asynchronous-requests-with-python-basehttpserver

# not sure flask is any better:
# https://blog.miguelgrinberg.com/post/video-streaming-with-flask


def compress(orig, comp):
	return float(orig) / float(comp)


class mjpgServer(BaseHTTPRequestHandler):
	"""
	A simple mjpeg server that either publishes images directly from a camera
	or republishes images from another pygecko process.
	"""

	cam = None
	ip = None
	hostname = None

	def setUpCamera(self, cv=None, pi=None, win=(320, 240)):
		"""
		cv - camera number, usually 0
		pi - set to True
		"""
		if pi:
			self.cam = Camera('pi')
			self.cam.init(win=win)
		elif cv:
			self.cam = Camera('cv')
			self.cam.init(cameraNumber=cv, win=win)

		else:
			raise Exception('Error, you must specify "cv" or "pi" for camera type')

	def getImage(self):
		if self.cam:
			print('cam')
			return self.cam.read()

		else:
			if not self.cam:
				raise Exception('Error, you must setup camera first')
			print('You should call setUpCamera() first ... let us try now and assume "cv=0"')
			self.setUpCamera(cv=0)
			return False, None

	# def do_HEAD(s):
	# 	print 'do_HEAD'
	# 	s.send_response(200)
	# 	s.send_header("Content-type", "text/html")
	# 	s.end_headers()

	def do_GET(self):
		print('connection from:', self.address_string())

		if self.ip is None or self.hostname is None:
			self.hostname = Socket.gethostname()
			self.ip = Socket.gethostbyname(Socket.gethostname())

		if self.path == '/mjpg':
			self.send_response(200)
			self.send_header(
				'Content-type',
				'multipart/x-mixed-replace; boundary=--jpgboundary'
			)
			self.end_headers()

			while True:
				# ret, img = capture.read()
				ret, img = self.getImage()
				if not ret:
					# print 'crap'
					time.sleep(1)
					continue

				ret, jpg = cv2.imencode('.jpg', img)
				# print 'Compression ratio: %d4.0:1'%(compress(img.size,jpg.size))
				self.wfile.write("--jpgboundary")
				self.send_header('Content-type', 'image/jpeg')
				# self.send_header('Content-length',str(tmpFile.len))
				self.send_header('Content-length', str(jpg.size))
				self.end_headers()
				self.wfile.write(jpg.tostring())
				time.sleep(0.05)

		elif self.path == '/':
			# hn = self.server.server_address[0]
			port = self.server.server_address[1]
			ip = self.ip
			hostname = self.ip

			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write('<html><head></head><body>')
			self.wfile.write('<h1>{0!s}[{1!s}]:{2!s}</h1>'.format(hostname, ip, port))
			self.wfile.write('<img src="http://{}:{}/mjpg"/>'.format(ip, port))
			self.wfile.write('<p>{0!s}</p>'.format((self.version_string())))
			self.wfile.write('<p>The mjpg stream can be accessed directly at:<ul>')
			self.wfile.write('<li><a href="http://{0!s}:{1!s}/mjpg"/>http://{0!s}:{1!s}/mjpg</a></li>'.format(ip, port))
			self.wfile.write('<li><a href="http://{0!s}:{1!s}/mjpg"/>http://{0!s}:{1!s}/mjpg</a></li>'.format(hostname, port))
			self.wfile.write('</p></ul>')
			self.wfile.write('<p>This only handles one connection at a time</p>')
			self.wfile.write('</body></html>')

		else:
			print('error', self.path)
			self.send_response(404)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write('<html><head></head><body>')
			self.wfile.write('<h1>{0!s} not found</h1>'.format(self.path))
			self.wfile.write('</body></html>')

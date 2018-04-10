from __future__ import print_function
from .convenience import translate
from .convenience import rotate
from .convenience import resize
from .convenience import skeletonize
from .convenience import auto_canny
from .Camera import Camera
from .Camera import SaveVideo
from .CameraCalibrate import CameraCalibration
from .meta import find_function
from .contours import sort_contours
from .contours import label_contour
from .paths import list_images
from .paths import list_files
from .paths import url_to_image
from .object_detection import non_max_suppression
from .utils import python_ver
from .utils import is_cv2
from .utils import is_cv3
from .utils import get_opencv_version

from .version import __version__
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2016 Kevin Walchko'
__author__ = 'Kevin J. Walchko'


if is_cv2():
	print('WARNING: OpenCV 2.x is detected, this library is designed to work with OpenCV 3.x')

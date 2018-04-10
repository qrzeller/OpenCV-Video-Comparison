
from setuptools.command.test import test as TestCommand
from setuptools.dist import Distribution
import os


class BinaryDistribution(Distribution):
	binary = False

	def is_pure(self):
		return self.binary


class BuildCommand(TestCommand):
	"""Build binaries/packages"""
	pkg = None
	test = True
	py2 = True
	py3 = True

	def run_tests(self):
		if not self.pkg:
			raise Exception('BuildCommand::pkg is not set')

		print('+----------------------------------')
		print('| Package: {}'.format(self.pkg))
		print('+----------------------------------')
		print('| Python 2: tests & build: {}'.format(self.py2))
		print('| Python 3: tests & build: {}'.format(self.py3))
		print('+----------------------------------\n\n')

		pkg = self.pkg
		print('Delete dist directory and clean up binary files')
		os.system('rm -fr dist')
		os.system('rm -fr build')
		os.system('rm -fr .eggs')
		# os.system('rm -fr {}.egg-info'.format(pkg))
		os.system('rm {}/*.pyc'.format(pkg))
		os.system('rm -fr {}/__pycache__'.format(pkg))

		if self.test:
			print('Run Nose tests')
			if self.py2:
				ret = os.system("unset PYTHONPATH; python2 -m nose -w tests -v test.py")
				if ret > 0:
					print('<<< Python2 nose tests failed >>>')
					return
			if self.py3:
				ret = os.system("unset PYTHONPATH; python3 -m nose -w tests -v test.py")
				if ret > 0:
					print('<<< Python3 nose tests failed >>>')
					return

		print('Building packages ...')
		print('>> Python source ----------------------------------------------')
		os.system("unset PYTHONPATH; python setup.py sdist")
		if self.py2:
			print('>> Python 2 ---------------------------------------------------')
			os.system("unset PYTHONPATH; python2 setup.py bdist_wheel")
		if self.py3:
			print('>> Python 3 ---------------------------------------------------')
			os.system("unset PYTHONPATH; python3 setup.py bdist_wheel")


class PublishCommand(TestCommand):
	"""Publish to Pypi"""
	pkg = None
	version = None

	def run_tests(self):
		if not self.pkg or not self.version:
			raise Exception('PublishCommand::pkg or version is not set')

		pkg = self.pkg
		version = self.version
		print('Publishing to PyPi ...')
		os.system("unset PYTHONPATH; twine upload dist/{}-{}*".format(pkg, version))

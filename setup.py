from distutils.core import setup
from setuptools import find_packages

setup (
    name='sendwithus',
    version='1.0.0',
    author='Matt Harris',
    author_email='matt@sendwithus.com',
    packages=find_packages(),
    scripts=[],
    url='http://pypi.python.org/pypi/sendwithus/',
    license='LICENSE.txt',
    description='Python API client for sendwithus.com',
    long_description=open('README.md').read(),
    test_suite="sendwithus.test",
)


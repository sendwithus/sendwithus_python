from distutils.core import setup

setup (
    name='SWUAPI',
    version='0.1',
    author='Matt Harris',
    author_email='matt@sendwithus.com',
    packages=['swuapi', 'swuapi.test'],
    scripts=['bin/swuapi.py',],
    url='http://pypi.python.org/pypi/SWUAPI/',
    license='LICENSE.txt',
    description='Python API client for sendwithus.com',
    long_description=open('README.txt').read(),
    install_requires=[],
)

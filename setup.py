from distutils.core import setup
from setuptools import find_packages

with open('README.md') as fp:
    long_description = fp.read()

setup(
    name='sendwithus',
    version='1.3.1',
    author='sendwithus',
    author_email='us@sendwithus.com',
    packages=find_packages(),
    scripts=[],
    url='https://github.com/sendwithus/sendwithus_python',
    license='LICENSE.txt',
    description='Python API client for sendwithus.com',
    long_description=long_description,
    test_suite="sendwithus.test",
    install_requires=[
        "requests >= 1.1.0",
        "six >= 1.8.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Communications :: Email"
    ]
)

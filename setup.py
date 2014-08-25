from distutils.core import setup
from setuptools import find_packages

setup(
    name='sendwithus',
    version='1.0.16',
    author='sendwithus',
    author_email='us@sendwithus.com',
    packages=find_packages(),
    scripts=[],
    url='https://github.com/sendwithus/sendwithus_python',
    license='LICENSE.txt',
    description='Python API client for sendwithus.com',
    long_description=open('README.md').read(),
    test_suite="sendwithus.test",
    install_requires=[
        "requests >= 1.1.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Communications :: Email"
    ]
)

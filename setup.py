from distutils.core import setup
from setuptools import find_packages

with open('README.md') as fp:
    long_description = fp.read()

setup(
    name='sendwithus',
    version='1.9.0',
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
        "requests >= 2.0.0",
        "six >= 1.9.0"
    ],
    extras_require={
        "test": [
            "pytest >= 3.0.5",
            "pytest-xdist >= 1.15.0"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Communications :: Email"
    ]
)

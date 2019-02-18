#!/usr/bin/env python
from setuptools import setup, find_packages


def main():
    setup(
        name='pyqt3wrapper',
        version='1.0',
        description='equivalent of pyqt3_wrapper',
        long_description=open("README.md").read(),
        url='',
        author='Nicolas Haziza',
        packages=find_packages(),
        scripts=['pyqt3wrapper/pyuic_pyqt3wrapper.py'],
        install_requires=['python>=2.7'])

if __name__ == '__main__':
    main()

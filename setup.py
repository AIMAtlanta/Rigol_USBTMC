"""
A simple PyUSBTMC-based interface for the Rigol DS1102E Oscilloscope.

"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='Rigol_USBTMC',
    version='0.0.2',
    description='A simple PyUSBTMC-based interface for the Rigol DS1102E Oscilloscope.',
    author='Kevin D. Nielson, Boddmg',
    author_email='',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    packages=find_packages(),
    keywords='usbtmc rigol',
    install_requires=[
        'python-usbtmc',
        'numpy',
        'pyusb'
    ],
)

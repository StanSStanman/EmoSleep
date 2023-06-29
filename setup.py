from setuptools import setup, find_packages
import os

__version__ = '0.0.1'
NAME = 'emosleep'
AUTHOR = 'Ruggero Basanisi'
MAINTEINER = 'Ruggero Basanisi'

setup(
    name=NAME,
    version=__version__,
    packages=find_packages(),
    author=AUTHOR,
    maintainer=MAINTEINER,
    description="Pipeline for EmoSleep project's data analysis",
    license='None',
    install_requires=['numpy',
                      'scipy',
                      'mne',
                      'xarray',
                      'matplotlib']
)

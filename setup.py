from setuptools import setup, find_packages
from os import path
# here = path.abspath(path.dirname(__file__))
# Get the long description from the README file
# with open(path.join(here, 'README.md'), encoding='utf-8') as f:
#    long_description = f.read()

setup(
    name='swipl',  # Required
    version='1.0.0',  # Required
    description='pyswipのProlog',  # Optional
    author='takenl2021',
    install_requires=[
        'regex'
    ],
    packages=['swipl'],  # Required
)

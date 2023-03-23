from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='reacthass',
    version='0.1.1',
    packages=['reacthass'],
    url='https://github.com/N4S4/reacthass',
    license='GPL-3.0 license',
    description='Homeassistant API automation helper',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Renato Visaggio',
)

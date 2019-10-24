from setuptools import setup
from setuptools import find_packages
import glob

with open('README.md', 'r') as readme:
    long_description = readme.read()


setup(
    name='c0n3shell',
    version='0.1',
    python_requires='>=3',
    packages=find_packages(),

    author='Lrk',
    author_email='sfxelrick@gmail.com',
    description='A simple to use, basic remote web shell client for CTF and Pentest',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/lrk/c0ne-shell',
    license="Apache License 2.0, see LICENSE",
    keywords='pwntools exploit ctf capture the flag binary wargame overflow stack heap defcon',

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache 2 License",
        "Environment :: Console",
        "Operating System :: OS Independent"
    ]
)

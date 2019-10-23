import setuptools

with open('README.md','r') as readme :
    long_description = readme.read()


setuptools.setup(
    name='c0n3-shell',
    version='0.1',
    scripts=['c0n3shell'],
    author='Lrk',
    author_email='sfxelrick@gmail.com',
    description='A simple to use, basic remote web shell client for CTF and Pentest',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/lrk/c0ne-shell',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache 2 License",
         "Operating System :: OS Independent"
    ]
)

from setuptools import setup
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='SimpleHTTPSAuthServer',
    version='1.1.0',
    description='HTTPS server with Basic authentication and client certificate authentication',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/oza6ut0ne/SimpleHTTPSAuthServer',
    author='Ryota Okimatsu',
    author_email='oza6ut0ne@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    py_modules=['SimpleHTTPSAuthServer']
)

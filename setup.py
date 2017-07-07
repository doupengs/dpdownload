# coding: utf-8

from setuptools import setup
from dpdownload import __version__


long_description = '''
     _           _                     _                 _ 
  __| |_ __   __| | _____      ___ __ | | ___   __ _  __| |
 / _` | '_ \ / _` |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |
| (_| | |_) | (_| | (_) \ V  V /| | | | | (_) | (_| | (_| |
 \__,_| .__/ \__,_|\___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|
      |_| 
      
http://www.xicidaili.com/nn/1  -->  download proxy

Based on requests:
  Load the proxy file
  Automatic replacement agent
'''

setup(
    name="dpdownload",
    version=__version__,
    author="doupeng",
    author_email="doupeng1993@sina.com",
    url="https://github.com/doupengs/dpdownload",
    packages=['dpdownload'],
    description="Automatically replace the agent's downloader",
    long_description=long_description,
    license="Apache License 2.0",
    platforms=["Linux", "Windows"],
    install_requires=[
            'requests',
            'dplog>=0.0.3',
    ],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Intended Audience :: Developers",
        "License :: Apache License 2.0",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ]
)

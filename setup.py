"""
setup.py
"""

from setuptools import setup, find_packages

setup(
    name='logtime-cli',
    version='2.0.0',
    python_requires='>=2.6,<4',
    scripts=['lt', 'logtime'],
    packages=find_packages(),
    description='CLI utility for logging the time you spend on things',
    author='Kyle Fitzpatrick',
    author_email='kyle.a.fitzpatrick@gmail.com',
    url='https://github.com/K-Fitzpatrick/logtime-cli',
    include_package_data=True,
    install_requires=[
        'click==6.7',
        'matplotlib==2.2.4',

        # Python 2/3 compatibility
        'future==0.17.1',
        'configparser==3.8.1',
    ],
)

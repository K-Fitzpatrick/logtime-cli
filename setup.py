from setuptools import setup

setup(
    name='logtime-cli',
    version='0.6.0',
    scripts=['lt'],
    packages=['logtime_cli'],
    description='CLI utility for logging the time you spend on things',
    author='Kyle Fitzpatrick',
    author_email='kyle.a.fitzpatrick@gmail.com',
    url='https://github.com/K-Fitzpatrick/logtime-cli',
    include_package_data=True,
    install_requires=[
        'click==6.7'
    ],
)

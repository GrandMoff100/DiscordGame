from setuptools import setup
import requests
import datetime
import subprocess
import sys
import os

__project_name__ = 'DiscordGame'

with open('README.md', encoding='utf-8') as file:
    long_description = file.read()

__project_url__ = f'https://pypi.python.org/pypi/{__project_name__}/json'

__old_version__ = requests.get(__project_url__).json()
__old_version__ = __old_version__['info']['version']

now = datetime.datetime.now()

__new_version__ = '{}.{}.{}'.format(now.year, now.month, now.day)

if __new_version__.split('.') == __old_version__.split('.')[:2]:
    __new_version__ = '.'.join(*__new_version__.split('.'), str(int(__old_version__.split('.')[3]) + 1))
else:
    __new_version__ = '.'.join([*__new_version__.split('.'), '0'])


setup(
    name=__project_name__,
    version=__new_version__,
    packages=['discordgame'],
    url='https://github.com/GrandMoff100/Discordgame',
    license='GNU License',
    author='Pixymon',
    author_email='nlarsen23.student@gmail.com',
    install_requires=['discord', 'requests'],
    description='A Python Discord Library for developing games in Discord Servers.',
    long_description=long_description,
    long_description_content_type='text/markdown'
)

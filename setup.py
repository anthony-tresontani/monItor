import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='monitor',
      version='0.1.0',
      description='Check script scheduler',
      long_description =read('README.txt'),
      author='Anthony Tresontani',
      author_email='dev.tresontani@gmail.com',
      packages=['monitor', 'run-check', 'notifier','setup', 'config'],
      include_package_data=True,
      scripts = ['run-check.py'],
      install_requires = ['SQLAlchemy==0.7.6','']
     )

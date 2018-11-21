import codecs
import os
import re
from distutils.core import setup
from glob import glob
from os.path import basename, splitext

from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name='zpi',
    version=find_version("src", "zpi", "version.py"),
    url='https://github.com/getzoop/python-infra-endpoints',
    license='MIT',
    author='Renan Chagas',
    author_email='renan.chagas@zoop.co',
    package_dir={'zpi': 'src/zpi'},
    packages=find_packages('src'),
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    description='Monitoring tools for python application.',
    python_requires='>=3.6',
    zip_safe=False,
    entry_points="""
      [console_scripts]
      zpi-increment-version = zpi.increment_version:main
      """,
    install_requires=[
        "PyYAML",
        "stringcase"
    ]
)

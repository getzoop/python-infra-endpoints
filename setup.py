from distutils.core import setup
from glob import glob
from os.path import basename, splitext

from setuptools import find_packages

import src.infrastructure

setup(
    name='zpi',
    version=src.infrastructure.__version__,
    url='https://github.com/getzoop/python-infra-endpoints',
    license='MIT',
    author='Renan Chagas',
    author_email='renan.chagas@zoop.co',
    package_dir={'infrastructure': 'src/infrastructure'},
    packages=find_packages('src'),
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    description='Monitoring tools for python application.',
    python_requires='>=2.7',
    zip_safe=False,
    install_requires=[
        "PyYAML",
        "stringcase"
    ]
)

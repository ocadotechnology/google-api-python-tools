from setuptools import find_packages
from setuptools import setup

import dataproc

if __name__ == '__main__':
    setup(name='DataProc-Python',
          description='Python client for Google DataProc.',
          url='https://github.com/ocadotechnology/dataproc-python',
          version=dataproc.__version__,
          license='Apache',
          keywords=['dataproc', 'python'],
          packages=find_packages(),
          include_package_data=True,
          install_requires=['python-dateutil'],
          tests_require=['nose'],
          test_suite="nose.collector",
          author=dataproc.__author__,
          classifiers=[
              'Intended Audience :: Developers',
              'Operating System :: OS Independent',
              'Programming Language :: Python',
          ])

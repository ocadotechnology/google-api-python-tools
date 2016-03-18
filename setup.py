from setuptools import setup

import google_api_python_tools

if __name__ == '__main__':
    setup(name='google-api-python-tools',
          description='Set of tools for Google services like DataProc.',
          url='https://github.com/ocadotechnology/google-api-python-tools.git',
          version=google_api_python_tools.__version__,
          license='Apache',
          keywords=['dataproc', 'python'],
          packages=['google_api_python_tools'],
          include_package_data=True,
          install_requires=['python-dateutil', 'oauth2client==1.5.2', 'google-api-python-client==1.3.1'],
          tests_require=['nose', 'mock'],
          test_suite="nose.collector",
          author=google_api_python_tools.__author__,
          classifiers=[
              'Intended Audience :: Developers',
              'Operating System :: OS Independent',
              'Programming Language :: Python',
          ])

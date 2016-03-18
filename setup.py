from setuptools import setup

import google_api_python_tools

with open('README.rst') as readme_file:
    readme = readme_file.read()


if __name__ == '__main__':
    setup(name='google-api-python-tools',
          description='Set of tools for Google services like DataProc.',
          long_description=readme,
          url='https://github.com/ocadotechnology/google-api-python-tools.git',
          version=google_api_python_tools.__version__,
          license='Apache 2.0',
          keywords=['dataproc', 'python'],
          packages=['google_api_python_tools'],
          include_package_data=True,
          install_requires=['python-dateutil', 'oauth2client==1.5.2', 'google-api-python-client==1.3.1'],
          tests_require=['nose', 'mock'],
          test_suite="nose.collector",
          author=google_api_python_tools.__author__,
          classifiers=[
              'Development Status :: 2 - Pre-Alpha',
              'Natural Language :: English',
              'Programming Language :: Python',
              "Programming Language :: Python :: 2",
              'Programming Language :: Python :: 2.6',
              'Programming Language :: Python :: 2.7',
              'Intended Audience :: Developers',
              'Operating System :: OS Independent'
          ])

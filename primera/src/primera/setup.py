from setuptools import setup, find_packages

setup( name="primera_new_test",
      version="0.0.1",
      description="primera python packages test",
      packages=find_packages(),
      entry_points= {

          'console_scripts': [

              'primera=primera.main:main',

              ]
          }
      )

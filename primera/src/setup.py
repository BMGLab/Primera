from setuptools import setup, find_packages

setup( name="primera_test",
      version="0.0.1",
      description="primera python packages test",
      packages=find_packages(),

      entry_points= {

          'console_scripts': [
                
              'primera_filter_psl=tools.filter:main',
              'primera_prepare_primers=tools.preparePrimers:main',
              'primera_match_primers=tools.matchPrimers:main',
              'primera_filter_bed=tools.filter_bed:main'

              ]
          }

      )

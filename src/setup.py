from setuptools import setup, find_packages

setup( name="primera_test",
      version="0.0.2",
      description="primera python packages test",
      packages=find_packages(),

      entry_points= {

          'console_scripts': [
                
              'primera_filter_psl=tools.filter:main',
              'primera_match_primers=tools.matchPrimers:main',
              'primera_run_primer3=tools.run_Primer3:main',
              'primera_filter_bed=tools.filterBED:main',
              'primera_extract=tools.Extract:main',
              'primera_to_bed=tools.writeToBED:main',

              ]
          }

      )

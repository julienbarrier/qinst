from setuptools import setup, find_packages

setup(name='qinst',
      version='0.0.1',
      description='instrument drivers to use with qcodes',
      url='https://github.com/julienbarrier/qinst',
      author='Julien Barrier',
      author_email='julien.barrier@manchester.ac.uk',
      classifiers=[
          'Intended Audience :: Science/Research',
          'Programming Language :: Python :: 3 :: Only',
          'License :: Apache License',
          'Topic :: Scientific/Engineering',
      ],
      license='MIT',
      packages=find_packages(),
      python_requires='>=3.9',
      zip_safe=False)

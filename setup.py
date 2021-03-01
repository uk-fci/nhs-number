from setuptools import setup, find_packages

VERSION = '1.2.1'

setup(
    name='nhs_number',
    version=VERSION,
    py_modules=['nhs_number'],
    packages=find_packages(include=['nhs_number']),
    url='https://github.com/andylaw/NhsNumberChecks',
    download_url='https://github.com/andylaw/NhsNumberChecks/tarball/{}'.format(VERSION),
    license='MIT',
    author='Andy Law',
    author_email='andy.law@roslin.ed.ac.uk',
    description='Python library for checking the validity of NHS Numbers',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
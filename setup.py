from setuptools import setup, find_packages
from os import path
from io import open


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    readme = f.read()

with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requires = [req.strip() for req in f if req]


setup(
    name='ventu',
    version='0.4.5',
    author='Keming Yang',
    author_email='kemingy94@gmail.com',
    description=('Host your deep learning models easily.'),
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/kemingy/ventu',
    packages=find_packages(exclude=['examples*', 'tests*']),
    package_data={
    },
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
    install_requires=requires,
    zip_safe=False,
    entry_points={
        'console_scripts': [],
    },
)

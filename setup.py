from setuptools import setup, find_packages


setup(
    packages=find_packages(exclude=('tests',)),
    setup_requires=[
        'pytest-runner>=2.0'
    ],
    tests_require=[
        'pytest>=3.0',
        'pytest-cov>=2.4'
    ]
)

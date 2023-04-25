from setuptools import setup, find_packages

setup(
    name='turingo',
    version='2.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
        'PyMongo'
    ],
)

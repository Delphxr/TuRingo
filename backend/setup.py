from setuptools import setup, find_packages

setup(
    name='turingo',
    version='1.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
        'PyMongo'
    ],
)

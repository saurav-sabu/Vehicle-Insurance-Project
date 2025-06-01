# Import necessary functions from setuptools
from setuptools import setup, find_packages

# Configure the package setup
setup(
    name = "src",  # Name of the package
    version= "0.0.1",  # Version of the package
    author="Saurav Sabu",  # Author's name
    author_email="saurav.sabu9@gmail.com",  # Author's email
    packages=find_packages()  # Automatically find all packages and subpackages
)
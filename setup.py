import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="mylogger",
    version="0.0.1",
    description="Log into stdout, file and buffer automatically.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/jtorre94/mylogger",
    author="torre.preciado",
    author_email="torre.preciado@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=['mylogger'],
    install_requires=[
        'PyYAML==6.0'
    ],
    include_package_data=True,
)
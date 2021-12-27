import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pdfpam",
    version="1.1.0",
    description="Pick n' Mix to select and combine pages from multiple PDFs into one",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/jj-style/pdfpam",
    author="JJ Style",
    author_email="style.jj@protonmail.com",
    license="GNU General Public License v3 (GPLv3)",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages=["pdfpam"],
    include_package_data=True,
    install_requires=["click"],
    entry_points={
        "console_scripts": [
            "pdfpam=pdfpam.main:main",
        ]
    },
)

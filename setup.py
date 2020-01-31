import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="geoutils3D",
    version="0.2.2",
    author="N. Wichmann",
    author_email="-", #T.B.D.
    description="Utilities for 3D geometry operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/microGen/GeoUtils3D",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
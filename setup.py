from setuptools import setup
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="maskpass",
    version="0.3.0",
    description="getpass alternative with masking, Spyder support and additional features ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FuturisticGoo/maskpass",
    author="Aman Anifer",
    author_email="fgoo.edu@hash.fyi",
    license="MIT",
    keywords=["password","cryptography","getpass","getpass3","mask","spyder","input","pynput"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=["maskpass"],
    include_package_data=True,
    install_requires=[],
    
)

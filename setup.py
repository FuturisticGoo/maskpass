import setuptools as s

with open("README.md", "r") as fh:
    long_description = fh.read()

s.setup(
    name="maskpass",
    version="0.1.0",
    description="A simple getpass alternative with masking feature",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FuturisticGoo/maskpass",
    author="Aman Anifer",
    author_email="amananiferfiaff@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
        "Operating System :: OS Independent",
    ],
    packages=["maskpass"],
    include_package_data=True,
    install_requires=s.find_packages(),
    
)

with open("README.md", "r") as fh:
    long_description = fh.read()

s.setup(
    name="maskpass",
    version="0.2.0",
    description="getpass alternative with masking and additional features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FuturisticGoo/maskpass",
    author="Aman Anifer",
    author_email="amananiferfiaff@gmail.com",
    license="MIT",
    keywords=["password","cryptography","getpass","getpass3","mask","spyder","input"]
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=["maskpass"],
    include_package_data=True,
    install_requires=[],
    
)

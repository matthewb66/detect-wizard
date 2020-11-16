import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="detect-wizard",
    version="1.0-Beta-10",
    author="Matthew Brady, Jay Ricco, Jaclyn Kaplan, Damon Weinstein",
    author_email="w3matt@gmail.com",
    description="Black Duck scanning wizard to pre-scan folders, determine optimal scan configuration and call Synopsys Detect to scan",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matthewb66/detect-wizard",
    packages=setuptools.find_packages(),
    install_requires=['python-magic',
                      'blackduck',
                      'texttable'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    scripts=['bin/detect-wizard'],
)

import setuptools
import platform

platform_system = platform.system()

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="detect_wizard",
    version="1.0-Beta-21",
    author="Matthew Brady, Jay Ricco, Jaclyn Kaplan, Damon Weinstein",
    author_email="w3matt@gmail.com",
    description="Black Duck scanning wizard to pre-scan folders, determine optimal scan configuration and call Synopsys Detect to scan",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matthewb66/detect-wizard",
    packages=setuptools.find_packages(),
    install_requires=['libmagic',
                      'python-magic>=0.4.15',
                      'blackduck>=0.0.55',
                      'texttable>=1.4.0',
                      'python-magic-bin>=0.4.14 ; platform_system=="Windows"'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': ['detect-wizard=detect_wizard_src.detect_wizard:run'],
    },
)

from setuptools import find_package, setup

setup(
    name = "atelier",
    version = "0.0.1",
    author = "IFFranciscoME",
    author_email = "if.francisco.me@gmail.com",
    description = "A Workshop for Synthetic A.I.",
    long_description = "A virtual workshop for cognitive training on synthetic artificial intelligence",
    url = "https://github.com/lucidmode/atelier",
    install_requires = [],
    packages = find_packages(exclude=("tests",)),
    classifiers = [
        "development status :: 4 - Beta",
        "Programming language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires = '>=3',
    test_require = ['pytest'],
)

from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name='glossarpy',
    version='0.0.2',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ash O'Farrrell",
    author_email='aofarrel@ucsc.edu',
    packages=['glossarpy'],
    url='https://github.com/aofarrel/glossarpy.git',
    platforms=["MacOS X", "Posix"],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Documentation",
        "Topic :: Text Processing :: Markup :: reStructuredText"
    ]
)
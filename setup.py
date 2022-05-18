from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name='glossarpy',
    version='0.0.3',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ash O'Farrrell",
    author_email='aofarrel@ucsc.edu',
    packages=['glossarpy'],
    include_package_data=True,
    package_data={"glossarpy": ["*.md", "*.pyi"]},
    zip_safe=False,  # required for mypy to find glossarpy.pyi... but doesn't seem to be working
    url='https://github.com/aofarrel/glossarpy.git',
    platforms=["MacOS X", "Posix"],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Documentation",
        "Topic :: Text Processing :: Markup :: reStructuredText"
    ]
)
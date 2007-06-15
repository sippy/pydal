from setuptools import setup, find_packages
setup(
    name = "dal",
    version = "0.2",
    packages = find_packages(),
    scripts = [],
    zip_safe = True,

    # metadata for upload to PyPI
    author = "Randall Smith",
    author_email = "randall@tnr.cc",
    description = "a python database abstraction layer.",
    license = "BSD",
    keywords = "dal",
    url = "http://pydal.sourceforge.net/",
)

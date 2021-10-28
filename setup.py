import setuptools

with open("bagoftricks/about.py") as f:
    v = f.read()
    for l in v.split("\n"):
        if l.startswith("__version__"):
            __version__ = l.split('"')[-2]

with open("readme.md", encoding="utf-8") as f:
    long_description = f.read()


setuptools.setup(
    name="bagoftricks",
    version=__version__,
    description="Kenneth Enevoldsen's utility functions",
    license="Apache License 2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Kenneth C. Enevoldsen",
    author_email="kennethcenevoldsen@gmail.com",
    url="https://github.com/KennethEnevoldsen/bagoftricks",
    packages=setuptools.find_packages(),
    include_package_data=True,
    # external packages as dependencies
    install_requires=["coolname==1.1.0"],
    keywords="utilities",
)
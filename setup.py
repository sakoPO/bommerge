import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bommerger",
    version="0.0.1",
    author="Pawel Okas",
    author_email="sako.po@gmail.com",
    description="BOM Merging Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sakoPO/bommerge",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: BSD-3 License",
        "Operating System :: OS Independent",
    ),
)

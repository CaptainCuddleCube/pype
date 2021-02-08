import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pype",
    version="0.0.1",
    author="Ashton Hudson",
    description="pype lets you create simple data pipelines in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=["httpx>=0.16.1"],
    tests_requires=[],
    extras_require={"dev": ["pylint==2.6.0", "black==20.8b1"]},
)

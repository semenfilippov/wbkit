import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wbkit",
    version="0.0.4",
    author="semenfilippov",
    author_email="semenfilippov@gmail.com",
    description="Aircraft weight and balance framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/semenfilippov/wbkit",
    project_urls={
        "Bug Tracker": "https://github.com/semenfilippov/wbkit/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src", exclude=["tests"]),
    python_requires=">=3.10",
    install_requires=["numpy>=1.22,<2"],
)

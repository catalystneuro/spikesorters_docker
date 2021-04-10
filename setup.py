from setuptools import setup, find_packages

d = {}
exec(open("spikesorters_docker/version.py").read(), None, d)
version = d['version']
long_description = open("README.md").read()

pkg_name = "spikesorters_docker"

setup(
    name=pkg_name,
    version=version,
    author="Alessio Buccino",
    author_email="alessiop.buccino@gmail.com",
    description="Test package for dockerized spike sorters",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/catalistneuro/spikesorters_focker",
    packages=find_packages(),
    package_data={},
    include_package_data=True,
    install_requires=[
        'numpy',
        'spikeextractors',
        'spikesorters',
        'hither'
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    )
)

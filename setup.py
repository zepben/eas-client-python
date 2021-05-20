from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="zepben.eas",
    version="0.1",
    description="Python SDK for interacting with the Evolve App Server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/zepben/eas-python-client",
    author="Ramon Bouckaert",
    author_email="ramon.bouckaert@zepben.com",
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src", include="zepben.*"),
    python_requires='>=3.7'
)

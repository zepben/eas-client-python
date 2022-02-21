#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

test_deps = ["pytest", "pytest-cov", "pytest-httpserver==1.0.4", "trustme==0.9.0"]
setup(
    name="zepben.eas",
    version="0.7.0b2",
    description="Python SDK for interacting with the Evolve App Server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/zepben/eas-python-client",
    author="Ramon Bouckaert",
    author_email="ramon.bouckaert@zepben.com",
    package_dir={"": "src"},
    python_requires='>=3.7',
    packages=find_namespace_packages(where="src"),
    install_requires=[
        "geojson==2.5.0",
        "requests==2.26.0",
        "urllib3==1.26.6",
        "zepben.auth==0.7.0b2",
    ],
    extras_require={
        "test": test_deps,
    }
)

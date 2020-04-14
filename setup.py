#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import os

from setuptools import find_packages, setup

from m2r import parse_from_file


def parse_reqs(filepath):
    with open(filepath, "r") as f:
        reqstr = f.read()
    requirements = []
    for line in reqstr.splitlines():
        line = line.strip()
        if line == "":
            continue
        elif not line or line.startswith("#"):
            # comments are lines that start with # only
            continue
        elif line.startswith("-r") or line.startswith("--requirement"):
            _, new_filename = line.split()
            new_file_path = os.path.join(os.path.dirname(filepath or "."), new_filename)
            requirements.extend(parse_reqs(new_file_path))
        elif line.startswith("-f") or line.startswith("-i") or line.startswith("--"):
            continue
        elif line.startswith("-Z") or line.startswith("--always-unzip"):
            continue
        else:
            requirements.append(line)
    return requirements


version = "0.1.0"
readme = open("README.rst").read()
history = parse_from_file("CHANGELOG.md")
requirements = parse_reqs("requirements.txt")
test_requirements = parse_reqs("requirements/test.txt")

setup(
    author="Data Science Team",
    author_email="you@chrobinson.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="",
    install_requires=requirements,
    include_package_data=True,
    long_description=readme + "\n\n" + history,
    keywords="rules",
    name="rules",
    packages=find_packages(
        exclude=["example*", "tests*", "docs", "build"],
        include=["rules"],
    ),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/Python Rules/rules",
    version=version,
    zip_safe=False,
)

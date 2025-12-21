"""
Setup configuration for Jarvis Home Automation System
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="jarvis-home",
    version="0.1.0",
    author="Keith Jasper",
    description="A comprehensive home automation platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/keithjasper83/Jarvis-Home",
    project_urls={
        "Bug Tracker": "https://github.com/keithjasper83/Jarvis-Home/issues",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Home Automation",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "jarvis=jarvis.main:main",
        ],
    },
)

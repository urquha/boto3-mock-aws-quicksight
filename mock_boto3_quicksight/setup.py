import sys

from setuptools import setup

assert sys.version_info >= (3, 6, 0), "mock_boto3_quicksight requires Python 3.6+"
from pathlib import Path  # noqa E402

CURRENT_DIR = Path(__file__).parent
sys.path.insert(0, str(CURRENT_DIR))  # for setuptools.build_meta

setup(
    name="mock_boto3_quicksight",
    description="A logging library to standardise log formats in JSON format",
    url="https://github.com/urquha/boto3-mock-aws-quicksight",
    license="MIT",
    packages=["mock_boto3_quicksight"],
    package_dir={"": "."},
    package_data={"mock_boto3_quicksight": ["py.typed"]},
    python_requires=">=3.6",
    test_suite="tests",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
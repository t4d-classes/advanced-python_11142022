"""Setup Package Module"""

from pathlib import Path
from setuptools import find_packages, setup

HERE = Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="rates_client",
    version="0.1.0",
    description="Rates app client",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://www.t4d.io",
    license="MIT",
    author="Eric",
    author_email="eric@t4d.io",
    packages=find_packages(where=".", exclude=('tests',))
)

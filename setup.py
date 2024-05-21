from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="newport_laser_diode_driver",
    description="Python library for interfacing with Newport Model 300-500B Series Laser Diode Driver",
    version="1.0.5",
    author="NextZtepS",
    author_email="natdanaiongarjvaja@gmail.com",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "pyusb",
    ],
    extras_require={
        "dev": [
            "pytest",
            "twine",
        ],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NextZtepS/newport_laser_diode_driver",
    license="MIT",
)
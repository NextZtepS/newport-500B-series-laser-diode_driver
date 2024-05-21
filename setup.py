from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='newport_laser_diode_driver',
    version='1.0.2',
    license="MIT",
    packages=find_packages(),
    install_requires=[
        'pyusb',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
)
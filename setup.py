from setuptools import setup, find_packages
from typing import List

HYPEN_E_DOT = '-e .'

def get_requirements(file_path: str) -> List[str]:
    """This function returns the list of requirements"""
    # Read lines, strip whitespace, ignore empty lines and comments.
    with open(file_path) as file_obj:
        requirements = [line.strip() for line in file_obj if line.strip() and not line.strip().startswith('#')]

    # Remove editable install marker if present
    if HYPEN_E_DOT in requirements:
        requirements.remove(HYPEN_E_DOT)

    return requirements

setup(
    name='mlproject',
    version='0.1.0',
    author='Sunil Verma',
    author_email='sunilverma00027@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)

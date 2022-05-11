from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["python>=3.6"]

setup(
    name="PyTES",
    version="0.0.1",
    author="Jiachen Xu",
    author_email="jxu1809@gmail.com",
    description="A Python-toolbox for closed-loop transcranial electrical stimultion",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/TateXu/pytes",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: 3-clause BSD",
    ],
)

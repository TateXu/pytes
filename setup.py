from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

def gen_data_files(*dirs):
    results = []

    for src_dir in dirs:
        for root,dirs,files in os.walk(src_dir):
            results.append((root, map(lambda f:root + "/" + f, files)))
    print(results)
    return results

setup(
    name="pytes",
    version="0.0.1",
    author="Jiachen Xu",
    author_email="jxu1809@gmail.com",
    description="A Python-toolbox for closed-loop transcranial electrical stimultion",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/TateXu/pytes",
    packages=['pytes'],
    package_dir={'pytes': 'pytes/'},
    package_data={'pytes': ['example_data/*.pkl']},
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: 3-clause BSD",
    ],
    license="3-clause BSD",
    data_files = [('Figures', ['./Figures/*.png', './Figures/*.jpeg'])]
)

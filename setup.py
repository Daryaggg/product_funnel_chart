from setuptools import find_packages, setup
import os.path


def find_requires():
    # take requirements from file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, "requirements.txt"), "r") as reqs:
        requirements = reqs.readlines()
    return requirements


try:
    with open("README.md") as fp:
        readme = fp.read()
except FileNotFoundError:
    readme = ""


setup(
    name="product_funnel_chart",
    version="0.0.2",
    author="Darya Guselnikova",
    description="Makes a nice chart of a user funnel based on Plotly",
    long_description=readme,
    packages=find_packages(),
    python_requires=">=3.6",
    include_package_data=True,
    install_requires=find_requires()
)

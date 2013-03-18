from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()


setup(
    name="partial-include",
    version="1.0",
    author="Preston Timmons",
    url="https://github.com/prestontimmons/partial_include",
    description="A more powerful include tag for Django",
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
)

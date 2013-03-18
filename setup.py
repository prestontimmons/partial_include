from setuptools import setup, find_packages

f = open("README.md")

setup(
    name="Partial Include",
    version="1.0",
    author="Preston Timmons",
    url="https://github.com/prestontimmons/partial_include",
    description="A more powerful include tag for Django",
    long_description=f.read(),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
)

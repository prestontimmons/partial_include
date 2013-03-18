from setuptools import setup, find_packages

DESCRIPTION = """
A more powerful Django include tag.

* Works with recursive includes
* Allows templates to be conditionally included, based on whether they exist
* Allows individual blocks to be included from a template
* Backwards-compatible with the Django built-in include tag

See:

https://github.com/prestontimmons/partial_include
"""

setup(
    name="partial-include",
    version="1.0",
    author="Preston Timmons",
    url="https://github.com/prestontimmons/partial_include",
    description="A more powerful include tag for Django",
    long_description=DESCRIPTION,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
)

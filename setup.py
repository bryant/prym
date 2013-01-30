from setuptools import setup, find_packages

dependencies = ["werkzeug", "sqlalchemy", "jinja2"]

setup(
    name = "prym",
    version = "0.1",
    install_requires = dependencies,

    packages = find_packages(),
    test_suite = "tests"
)

from setuptools import setup

setup(
    name="rich-click",
    install_requires=[
        "click",
        "rich",
        "importlib-metadata; python_version < '3.8'",
    ],
)

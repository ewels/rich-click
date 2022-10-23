from setuptools import setup

setup(
    install_requires=[
        "click>=7",
        "rich>=10.7.0",
        "importlib-metadata; python_version < '3.8'",
        "typing_extensions",
    ],
    extras_require={
        "dev": ["pre-commit", "pytest", "flake8", "flake8-docstrings"],
    },
)

from setuptools import setup

setup(
    name="rich-click",
    install_requires=[
        "click>=7.0",
        "rich>=10",
    ],
    extras_require={
        "typer": "typer>=0.4",
    },
)

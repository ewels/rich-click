from setuptools import setup

setup(
    name="rich-click",
    install_requires=[
        "click>=7",
        "rich>=10.7.0",
        "importlib-metadata; python_version < '3.8'",
    ],
    extras_require={
        "typer": "typer>=0.4",
        "dev": "pre-commit",
    },
    package_data={"rich_click": ["py.typed"]},
)

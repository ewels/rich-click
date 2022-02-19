from setuptools import setup

setup(
    name="rich-click",
    entry_points={"console_scripts": ["rich-click = rich_click.cli:main"]},
    install_requires=[
        "click",
        "rich",
        "importlib-metadata; python_version < '3.8'",
    ],
)

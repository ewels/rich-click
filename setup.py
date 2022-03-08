from setuptools import setup

setup(
    name="rich-click",
    install_requires=[
        "click>=7",
        "rich>=10",
        "importlib-metadata; python_version < '3.8'",
    ],
    extras_require={
        "dev": ["pre-commit"],
    },
    package_data={"rich-click": ["py.typed"]},
)

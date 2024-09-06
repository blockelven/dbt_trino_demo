from setuptools import find_packages, setup

setup(
    name="downtown",
    version="0.0.1",
    packages=find_packages(),
    package_data={
        "downtown": [
            "dbt-project/**/*",
        ],
    },
    install_requires=[
        "dagster",
        "dagster-cloud",
        "dagster-dbt",
        "dbt-duckdb<1.9",
    ],
    extras_require={
        "dev": [
            "dagster-webserver",
        ]
    },
)
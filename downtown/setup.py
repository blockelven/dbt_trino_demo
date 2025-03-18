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
        "dagster==1.10.5",
        "dagster-dbt==0.26.5",
        "dbt-duckdb<1.10",
    ],
    extras_require={
        "dev": [
            "dagster-webserver==1.10.5",
        ]
    },
)


from pathlib import Path

from dagster_dbt import DbtProject

jaffle_shop_project = DbtProject(
    project_dir=Path(__file__).joinpath("..", "..", "..", "etl", "jaffle_shop").resolve(),
    packaged_project_dir=Path(__file__).joinpath("..", "..", "dbt-jaffle").resolve(),
)
jaffle_shop_project.prepare_if_dev()

stock_project = DbtProject(
    project_dir=Path(__file__).joinpath("..", "..", "..", "etl", "stock").resolve(),
    packaged_project_dir=Path(__file__).joinpath("..", "..", "dbt-stock").resolve(),
)
stock_project.prepare_if_dev()

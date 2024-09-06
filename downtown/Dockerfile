FROM python:3.11-bookworm AS builder

RUN mkdir -p /opt/dagster/dagster_home /opt/dagster/app /opt/dagster/local /opt/dagster/dagster_home/log /opt/dagster/app/requirements


RUN apt update && apt install -y gcc g++ libpq-dev git curl
COPY requirements.txt /opt/dagster/app

COPY downtown/downtown/__init__.py /opt/dagster/app/downtown/downtown
COPY downtown/setup.py downtown/pyproject.toml /opt/dagster/app

RUN cd /opt/dagster/app && \
  pip install -r requirements.txt && \
  pip install ".[dev]"

RUN ls -al /usr/local/bin

FROM python:3.11-bookworm

# 复制编译阶段生成的依赖
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/dagster* /usr/local/bin
COPY --from=builder /usr/local/bin/dbt /usr/local/bin

RUN mkdir -p /opt/dagster/app /opt/dagster/dagster_home /opt/dagster/etl

COPY --from=builder /opt/dagster/app/build /opt/dagster/app/build

COPY downtown/downtown /opt/dagster/app/downtown
COPY downtown/setup.py downtown/pyproject.toml /opt/dagster/app

COPY downtown/workspace_docker.yaml /opt/dagster/app/workspace.yaml
COPY downtown/dagster_docker.yaml /opt/dagster/dagster_home/dagster.yaml

COPY etl/jaffle_shop /opt/dagster/etl/jaffle_shop
COPY etl/stock /opt/dagster/etl/stock

ENV DAGSTER_HOME=/opt/dagster/dagster_home/
WORKDIR /opt/dagster/app

EXPOSE 3070

ENTRYPOINT ["dagster-webserver", "-h", "0.0.0.0", "-p", "3070"]

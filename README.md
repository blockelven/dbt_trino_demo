# DBT Trino Demo

演示使用 Trino 聚合网络数据, 清洗到 `Iceberg` , 最终数据写入 `Postgres`

## 前置条件

1. 本地安装好 docker compose
2. 解决好网络问题

## 安装流程

```bash
git clone git@github.com:blockelven/dbt_trino_demo.git
cd dbt_trino_demo
docker compose up -d
```

## 演示流程

打开 `http://127.0.0.1:3070/locations/downtown/jobs/create_scheme_job/playground`, 点击 `Launch Run` 新建相关表

打开 `http://127.0.0.1:3070/asset-groups`, 点击 `Materialize All` 查看运行状态

## 端口说明

| Port | Description |
| --- | --- |
| 5432 | PG |
| 3070 | Dagster WebServer |
| 8060 | Trino Web Console |
| 8063 | Trino Web Console |
| 9000 | MinIO Web Console |

## 相关账号密码

| service | host | username | password |
| --- | --- | --- | --- |
| postgres| localhost:5432 | ngods | ngods |
| trino | localhost:8060 | trino | trino |
| MinIO | localhost:9000 | minio | minio123 |

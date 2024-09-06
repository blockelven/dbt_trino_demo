# DBT Trino Demo

## 前置条件

1. 本地安装好 docker compose
2. 解决好网络问题

## 安装流程

```bash
git clone git@github.com:blockelven/dbt_trino_demo.git
cd dbt_trino_demo
docker compose up -d
```

## 端口说明

| Port | Description |
| --- | --- |
| 5432 | PG |
| 3070 | Dagster WebServer |
| 8060 | Trino Web Console |
| 8063 | Trino Web Console |
| 9000 | MinIO Web Console | 

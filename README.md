# Introduction

IAM Access Analyzer for Azure.

## Running locally

Set the environment variables used:

```sh
export TENANT_ID="<TENANT_ID>"
export CLIENT_ID="<CLIENT_ID>"
export CLIENT_SECRET="<CLIENT_SECRET>"
```

```
python main.py <subscription> <username> <num_hours> <resource_group_name>
```

## Setting log level

App is using [Loguru](https://loguru.readthedocs.io/en/stable/index.html) so all settings are configurable via environment variables.

For example to configure the log level:

```sh
export LOGURU_LEVEL="INFO"
```

```sh
export LOGURU_LEVEL="DEBUG"
```

## Run tests

```sh
pytest -v
```

## TODO

- handle paging
- add mutliple login support
- compare to existing roles
- add management group support
- create an azure package
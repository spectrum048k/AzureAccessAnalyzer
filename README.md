![](https://img.shields.io/github/license/spectrum048k/AzureAccessAnalyzer)
![](https://img.shields.io/github/repo-size/spectrum048k/AzureAccessAnalyzer)

# Azure Access Analyzer

This is an IAM Access Analyzer for Azure. It will return all the actions / permissions used by a given user or service principal between two dates at either subscription or resource group scope.

## Installation

todo

## Running locally

Set the environment variables used:

```sh
export TENANT_ID="<TENANT_ID>"
export CLIENT_ID="<CLIENT_ID>"
export CLIENT_SECRET="<CLIENT_SECRET>"
```

```sh
python main.py <subscription> <username> <num_hours> <resource_group_name>
```

## Configuration

### Setting log level

App is using [Loguru](https://loguru.readthedocs.io/en/stable/index.html) so all settings are configurable via environment variables.

For example to configure the log level:

```sh
export LOGURU_LEVEL="INFO"
```

```sh
export LOGURU_LEVEL="DEBUG"
```

## Running Tests

```sh
pytest -v
```

## Roadmap

- handle paging
- add mutliple login support
- compare to existing roles
- add management group support
- create an azure package

![](https://img.shields.io/github/license/spectrum048k/AzureAccessAnalyzer)
![](https://img.shields.io/github/repo-size/spectrum048k/AzureAccessAnalyzer)

# Azure Access Analyzer

This is an IAM Access Analyzer for Azure. It will return all the actions / permissions used by a given user or service principal between two dates at either subscription or resource group scope.

## Installation

This project requires [pipenv](https://pipenv.pypa.io/en/latest/index.html)

## Running locally

App uses the Azure Python SDK [DefaultCredentialClass](https://learn.microsoft.com/en-us/python/api/azure-identity/azure.identity.defaultazurecredential?view=azure-python).


If using a service principal the environment variables used are:

```sh
export AZURE_TENANT_ID="<TENANT_ID>"
export AZURE_CLIENT_ID="<CLIENT_ID>"
export AZURE_CLIENT_SECRET="<CLIENT_SECRET>"
```

```sh
pipenv run python main.py <subscription> <username> <num_hours> <resource_group_name>
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
pipenv run pytest -v
```

## Roadmap

- handle paging
- compare to existing roles
- add management group support

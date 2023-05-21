# Introduction

IAM Access Analyzer, but for Azure.

## Running locally

Set the environment variables used:

```sh
export TENANT_ID="<TENANT_ID>"
export CLIENT_ID="<CLIENT_ID>"
export CLIENT_SECRET="<CLIENT_SECRET>"
```

## Setting log level

App is using [Loguru](https://loguru.readthedocs.io/en/stable/index.html) so all settings are configurable via environment variables.

For example to configure the log level:

```sh
export LOGURU_LEVEL="INFO"
```

## WIP notes

### next up

- add verbose logging of http requests
- add command line arguments
- handle paging

### follow up

- add mutliple login 
- compare to existing roles
- add manageent group support
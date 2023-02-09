# Timeseries

This is an coding practice repository for a timeseries API using python, angular, mqtt and MongoDB.

![Tests](https://github.com/rcbop/python-timeseries/actions/workflows/ci.yaml/badge.svg)
&nbsp;&nbsp;[![Lint K8s manifests](https://github.com/rcbop/python-timeseries/actions/workflows/lint-k8s-manifests.yaml/badge.svg)](https://github.com/rcbop/python-timeseries/actions/workflows/lint-k8s-manifests.yaml)&nbsp;&nbsp;[![codecov](https://codecov.io/gh/rcbop/timeseries-visualization/branch/main/graph/badge.svg?token=ijcD6RzE8L)](https://codecov.io/gh/rcbop/timeseries-visualization)&nbsp;&nbsp;[![CodeQL](https://github.com/rcbop/python-timeseries/workflows/CodeQL/badge.svg)](https://github.com/rcbop/python-timeseries/actions/workflows/github-code-scanning/codeql)&nbsp;&nbsp;[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Frcbop%2Fpython-timeseries.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Frcbop%2Fpython-timeseries?ref=badge_shield)

## Requirements

- [Pyenv](https://github.com/pyenv/pyenv)
- [Pyenv virtualenv](https://github.com/pyenv/pyenv-virtualenv)
- `GNU make`

## Development

Run all tests with docker compose:

```
make test
```

Spin up development environment:

```
make compose-up
```

## Query String Filters

API endpoint with query string filters deep-object like:

```
?timestamp[gte]=2021-01-01T00:00:00&timestamp[lte]=2021-01-05T00:00:00&metadata.area=kitchen&limit=100"
```

will become mongo query:

```
{
    "timestamp": { $gte: ISODate("2021-01-01T00:00:00"), $lte: ISODate("2021-01-05T00:00:00") },
    "metadata": { "area": "kitchen" },
    "limit": 100
}
```

## Preview

### Default endpoint result:

Limits to 100 results:

![query-result](./docs/query-result.png)

### Angular Custom Dashboard:

![dashboard](./docs/dashboard.png)

### Plotly Dashboard:

![plotly-dashboard](./docs/plotly-dash.png)

### Filtering by query string example:

![using-query-string-filters](./docs/using-query-string-filters.png)

## Dependencies
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Frcbop%2Fpython-timeseries.svg?type=small)](https://app.fossa.com/projects/git%2Bgithub.com%2Frcbop%2Fpython-timeseries?ref=badge_small)

## TODO

- ~~API pagination offset~~ (done)
- ~~Pyparsing query validation~~ (done)
- check usage of [mongo engine ORM](http://mongoengine.org/) with timeseries collection
- [kube-linter](https://docs.kubelinter.io/#/) [does not support kustomize](https://github.com/stackrox/kube-linter/issues/113), pre-render manifests before running linter
- add UI tests (cypress)
- ~~increase test coverage~~ (done)
- instrumentation, tracing, metrics and monitoring
- terraform deployment

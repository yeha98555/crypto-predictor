# Crypto Price Predictor

## Environment
- Ubuntu 22.04
- Make 4.3
- Python 3.10
- Docker 26.1.4
- Docker Compose 2.25.1

## Setup
Take `trades` microservice as an example in Usage section.

### uv
[uv](https://docs.astral.sh/uv/): an extremely fast Python package and project manager.

#### Install
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Usage
Create a project with uv.
```sh
cd services
uv init [project-name]
# e.g. uv init trades
```
Then the folder structure will be created automatically.
```
services
├── trades
│   ├── .python-version   // the Python version used in the project
│   ├── hello.py          // a simple hello world program (the entry point of the project)
│   ├── pyproject.toml    // the configuration file for uv
│   └── README.md         // the README file
```
Usually change `hello.py` to `run.py` and write the main logic in `run.py`.

### Make
[Make](https://www.gnu.org/software/make/manual/make.html): a build automation tool.

#### Install
```sh
sudo apt install make
```
#### Usage
Write a Makefile in the project.
```sh
cd services/trades
make [target]
# e.g. make run
```

### Redpanda
[Redpanda](https://docs.redpanda.com/latest/): a fast, reliable, and cost-effective Kafka®-compatible event streaming platform.

#### Usage
Use the docker compose file in `docker-compose/redpanda.yml`.
And run the following command.
```sh
cd docker-compose
docker compose -f redpanda.yml up -d
```

### Pre-commit
[Pre-commit](https://pre-commit.com/): a framework for managing and maintaining multi-language pre-commit hooks.

#### Install
```sh
uv tool install ruff  # use ruff as the linter and formatter in pre-commit
uv tool install pre-commit
```
#### Usage
Install the git hooks scripts.
```sh
pre-commit install
# Ouput:
# pre-commit installed at .git/hooks/pre-commit
```
Then every time you commit, the hooks will be run automatically.

Or you can run against all the files manually, run the following command.
```sh
pre-commit run --all-files
```

## Steps

### Feature pipeline
- Ingest trades from external API
- Transform trades into technical indicators
- Save these technical indicators to a feature store

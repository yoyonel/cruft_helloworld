# cruft_helloworld

![PyPI](https://img.shields.io/pypi/v/cruft_helloworld?style=flat-square)
![GitHub Workflow Status (master)](https://img.shields.io/github/workflow/status/yoyonel/cruft_helloworld/Test%20&%20Lint/master?style=flat-square)
![Coveralls github branch](https://img.shields.io/coveralls/github/yoyonel/cruft_helloworld/master?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cruft_helloworld?style=flat-square)
![PyPI - License](https://img.shields.io/pypi/l/cruft_helloworld?style=flat-square)

Cruft Python Hello-World

## Requirements

* Python 3.7.3 or newer
* [poetry](https://poetry.eustance.io/) 1.1 or newer

## Installation

```sh
pip install cruft_helloworld
```

## Development

This project uses [poetry](https://poetry.eustace.io/) for packaging and
managing all dependencies and [pre-commit](https://pre-commit.com/) to run
[flake8](http://flake8.pycqa.org/), [isort](https://pycqa.github.io/isort/),
[mypy](http://mypy-lang.org/) and [black](https://github.com/python/black).

Clone this repository and run

```bash
poetry install
poetry run pre-commit install
```

to create a virtual environment containing all dependencies.
Afterwards, You can run the test suite using

```bash
poetry run pytest
```

This repository follows the [Conventional Commits](https://www.conventionalcommits.org/)
style.

### Pycharm debugging
[Debuggers and PyCharm](https://pytest-cov.readthedocs.io/en/latest/debuggers.html)
> Coverage does not play well with other tracers simultaneously running.
> This manifests itself in behaviour that PyCharm might not hit a breakpoint no matter what the user does.

### Cookiecutter template

This project was created using [cruft](https://github.com/cruft/cruft) and the
[cookiecutter-pyproject](https://github.com/escaped/cookiecutter-pypackage) template.
In order to update this repository to the latest template version run

```sh
cruft update
```

in the root of this repository.

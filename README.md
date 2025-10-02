# cfgts

CfGTS (Counterfactual Generation for Time Series) is a Python package designed to automatically generate counterfactuals for artificial intelligence models.

## Contributing
Please fork the project and clone it into your computer. Then install the required dependencies:
```sh
python -m venv .venv
```
```sh
. .venv/bin/activate
```
```sh
uv lock
```
```sh
just install
```
```sh
pre-commit install
```
then you can start linting
```sh
pre-commit
```
and testing
```sh
just test
```
# Exoplanet Hunt

This project aims to identify and analyze exoplanets using various algorithms and data analysis techniques.

## Installation

It is recommended to use a virtual environment to manage dependencies. To create and activate a virtual environment, run:

### On Windows

```bash
python -m venv exoplanet-env
exoplanet-env\Scripts\activate
```

### On macOS and Linux

```bash
python3 -m venv exoplanet-env
source exoplanet-env/bin/activate
```

Then, to install the package and required dependencies, run:

```bash
pip install .
```

Alternatively, you can install the dependencies directly using:

```bash
pip install -r requirements.txt
```

### Using setup.py

The `setup.py` file is used for packaging and distributing the project. It includes information about the package and its dependencies. To install the package using `setup.py`, run:

```bash
python setup.py install
```

This will install the package and its dependencies as defined in `setup.py`.

## Usage

To run the main application, use:

```bash
python src/main.py
```

## Testing

To run the tests, use:

```bash
pytest
```

## License

This project is licensed under the MIT License.

JII MultispeQ
=============

This Python package to access, transform and analyze MultispeQ data.

## Install

Install the package using [pip] in the terminal. As of now, the package is not distributed through [PyPI] so you are using [GitHub] as the source.

```shell
pip install git+https://github.com/Jan-IngenHousz-Institute/JII-MultispeQ.git --upgrade --no-cache-dir
```

**Note:** You will will find a detailed documentation inside the `docs/` folder.

## Development

The library is packaged using [SetupTools] with all settings inside the `pyproject.toml`. For more details check the SetupTools instructions.

### Local Development

The development version can be build use the command below, so you don't have to manually rebuild the package after a change.

```shell
pip install -e .
```

**Note:** You might require to run `python3` instead of `python`, depending on your system settings.

### Documentation

The documentation is using [Sphinx] with the [Furo] theme. You can find all the help documents in the subfolder `docs/source/`.

```shell
JII-MultispeQ/
├── docs/
│   ├── build/
│   ├── source/
│   │   ├── _static/
│   │   │   ├── downloads/
│   │   │   ├── examples/
│   │   │   └── images/
│   │   ├── _templates/
│   │   ├── conf.py
│   │   ├── index.rst
│   │   └── ...
│   ├── make.bat
│   └── Makefile
├── docs
├── src
├── tests
└── pyproject.toml
```

Use the command `make clean && make html` from inside the `docs/` folder to recompile the help.

[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/
[GitHub]: https://github.com/Jan-IngenHousz-Institute/
[SetupTools]: https://setuptools.pypa.io/
[Sphinx]: https://www.sphinx-doc.org/
[Furo]: https://github.com/pradyunsg/furo/
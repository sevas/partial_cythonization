
# partial_cythonization

Illustrate how to partially obfuscate a python package with cython

* Free software: MIT license

# Usage

```bash
python partial_cythonization/cli.py PKG_TO_OBFUSCATE DEST_DIR
```
with:
- `PKG_TO_OBFUSCATE`: the path to the package to obfuscate. This must be the top path to the imported package name.
- `DEST_DIR`: where to copy the obfuscated package. We will also copy the `"tests"` directory from the source dir if it exists.


# Features

* TODO


# Credits


This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

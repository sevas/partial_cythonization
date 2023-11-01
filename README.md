# partial_cythonization

Illustrate how to partially or completely obfuscate a python package with cython.

This is useful for the case where you want to distribute a package but do not want to share the source code, and get at least the same level of obfuscation as with a compiled language.

Note that even though we are using cython, do not expect huge speedups.
The compiled code will not be optimized, since no type annotations are added.
Nonetheless, the cython developers claim that you can get a [20%-50% speedup](https://cython.readthedocs.io/en/latest/src/tutorial/pure.html) on average.

# License
Free software: MIT license

# Usage

```bash
python partial_cythonization/cli.py PKG_TO_OBFUSCATE DEST_DIR
```

with:

- `PKG_TO_OBFUSCATE`: the path to the package to obfuscate. This must be the top path to the imported package name.
- `DEST_DIR`: where to copy the obfuscated package. We will also copy the `"tests"` directory from the source dir if it
  exists.

# Features

* Compile selected or all `.py` files to python extension files.
* Copy an obfuscated version of the package to a destination directory.

# Limitations

- If one of your module uses numba, this will likely not work.
- If you have you own `.pyx` files to compile with cython, you should compile them before running this tool.

# Credits

This package was created with [Cookiecutter][1] and the [audreyr/cookiecutter-pypackage][2] project template.


[1]: https://github.com/audreyr/cookiecutter

[2]: https://github.com/audreyr/cookiecutter-pypackage

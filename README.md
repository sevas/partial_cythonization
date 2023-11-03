# partial_cythonization

Illustrate how to partially or completely obfuscate a python package with cython.

This is useful for the case where you want to distribute a package but do not want to share the source code, and get at
least the same level of obfuscation as with language compiled with gcc/clang/cl.

Note that even though we are using cython, do not expect huge speedups.
The compiled code will not be optimized, since no type annotations are added.
Nonetheless, the cython developers claim that you can get
a [20%-50% speedup](https://cython.readthedocs.io/en/latest/src/tutorial/pure.html) on average.

# License

Free software: MIT license

# Usage

## Obfuscate selected files in a package

Invoking the following command:

```bash
python partial_cythonization/cli.py path/to/pkg_to_obfuscate path/to/obfuscated_pkg/destination
```

will look at all the source files in `pkg_to_obfuscate` and look for those with the following comment at the top:

```python
# obfuscate_with_cython: True

def foo(): ...


def bar(): ...
```

For each such file, it will compile the file to a python extension file and copy it to the destination directory.
Other source files will vbe copied as is.

## Obfuscate all eligible files in a package

By using the `-a` flag, all eligible files will be obfuscated.

```bash
python partial_cythonization/cli.py path/to/pkg_to_obfuscate path/to/obfuscated_pkg/destination -a

```

An eligible file is a file that:

- is a python source file with extension `.py`
- does not use `numba`
- is not ignored by the `always_exclude` rule in the configuration file

## Cleaning `.c` and `.pyd`/`.so` files

Since we build extensions in-place, after a successful run, the source package will contain `.c` files and corresponding `.pyd`/`.so`.

You may use the `-c`/`--clean` flag to remove them.


# Configuration

The configuration file is a `toml` file that must be passed to the command line with the `--cconfig` option.

It supports two keys:
- `include_data`: a list of file patterns for data files to be included in the obfuscated package.
- `always_exclude`: a list of file patterns for files to be excluded from the obfuscated package in every case.

```toml

include_data = [
    "*data/*.csv",
    "*.txt",
]

always_exclude = [
    "some_package/subpkg2/*"
]

```

# Features

* Compile selected or all `.py` files to python extension files.
* Copy an obfuscated version of the package to a destination directory.
* Detect source files using numba and skip them.
* Detect source files using cython and copy the compiled extension files, skipping the `.pyx`

# Limitations

- If one of your module uses numba, this will likely not work.
- If you have you own `.pyx` files to compile with cython, you should compile them before running this tool.

# Credits

This package was created with [Cookiecutter][1] and the [audreyr/cookiecutter-pypackage][2] project template.


[1]: https://github.com/audreyr/cookiecutter

[2]: https://github.com/audreyr/cookiecutter-pypackage

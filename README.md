# partial_cythonization

Illustrate how to partially or completely obfuscate a python package with cython.

This is useful for the case where you want to distribute a package but do not want to share the source code, and get at
least the same level of obfuscation as with a language compiled with gcc/clang/cl.

Note that even though we are using cython, do not expect huge speedups.
The compiled code will not be optimized, since no type annotations are added.
Nonetheless, the cython developers claim that you can get
a [20%-50% speedup](https://cython.readthedocs.io/en/latest/src/tutorial/pure.html) when compiling pure python files with cython.

The goal of this project is to share obfuscated code, not to speed up your code.

# License

Free software: MIT license

# Usage

## Obfuscate selected files in a package

Invoking the following command:

```bash
python partial_cythonization/cli.py path/to/repo_dir/pkg_to_obfuscate path/to/obfuscated_pkg_destination
```

will look at all the source files in `pkg_to_obfuscate` and look for those with the following comment at the top:

```python
# obfuscate_with_cython: True

def foo(): ...


def bar(): ...
```

For each such file, it will compile the file to a python extension file and copy it to the destination directory.
Other source files will be copied as is.

## Obfuscate all eligible files in a package

By using the `--compile-all`/`-a` flag, all eligible files will be obfuscated.

```bash
python partial_cythonization/cli.py path/to/repo_dir/pkg_to_obfuscate path/to/obfuscated_pkg_destination -a
cd path/to/repo_dir
export PYTHONPATH=path/to/obfuscated_pkg_destination
pytest tests/ -v
```

An eligible file is a file that:

- is a python source file with extension `.py`
- does not use `numba`
- is not ignored by the `always_exclude` rule in the configuration file

## Cleaning `.c` and `.pyd`/`.so` files

Since we build extensions in-place, after a successful run, the source package will contain `.c` files and corresponding `.pyd`/`.so`.

You may use the `-c`/`--clean` flag to remove them.

# How to make sure that the resulting package works the same as the original one?

The best way to make sure that the resulting package works the same as the original one is to run the tests. This program will copy the `tests/` folder in the destination dir, if it exists. These tests should be runnable with the obfuscated package the same way you run them on the original package, assuming tests source files are relocatable.

If the tests are not relocatable, we do not provide a turn-key solution.
You may however run the original test suite by changing the `PYTHONPATH` variable to point to the obfuscated package directory instead of the original one in the source tree.

For instance:

```bash
python partial_cythonization/cli.py path/to/repo_dir/pkg_to_obfuscate path/to/obfuscated_pkg_destination
cd path/to/repo_dir
export PYTHONPATH=path/to/obfuscated_pkg_destination
pytest tests/ -v
```

# Configuration

The configuration file is a `toml` file that must be passed to the command line with the `--config` option.

It supports two keys:
- `include_data`: a list of file patterns for data files to be included in the obfuscated package.
- `always_exclude`: a list of file patterns for files to be excluded from the obfuscated package in every case.
- `never_obfuscate`: a list of file patterns for files that should never be obfuscated with cython.

```toml

include_data = [
    "*data/*.csv",
    "*.txt",
]

always_exclude = [
    "some_package/subpkg2/*"
]

never_obfuscate = [
    # usually, no added value to obfuscate these files
    "*/__init__.py",
]

```

# Features

* Compile selected or all `.py` files to python extension files.
* Copy an obfuscated version of the package to a destination directory.
* Detect source files using numba and skip them.
* Detect source files using cython and copy the compiled extension files, skipping the `.pyx`

# Limitations

* If one of your module uses numba, this will likely not work.
* If you have you own `.pyx` files to compile with cython, you should compile them before running this tool.

Additionally, this tool is not intended to package a python program with all its
dependencies as a stand-alone redistributable.
It does not intend to replace tools such as [PyInstaller](https://pyinstaller.org/en/stable/), [Py2App](https://py2app.readthedocs.io/en/latest/), [cx_freeze](https://cx-freeze.readthedocs.io/en/stable/)
etc.

However, it can be used to pre-process a collection of packages to be then included in such a redistributable.


# Writing cython-compatible python code

## Discovery of modules by name

Any dynamic discovery of python modules should not only filter using the `".py"` file suffix.
For the equivalent code to work after conversion with cython, you must also handle native file suffix such as `".cpXYY-platform_arch.pyd"`.

In python, you can know the extension that cython will use with:
```python
import sysconfig
sysconfig.get_config_var("EXT_SUFFIX")
```

## Strict typechecking

If you use python type annotations, the generated cython code will use them to add
runtime type checking.

```python
def foo(a: int, b: int): ...

foo(3.2, 12)    # No error in pure python, but TypeError will be raised after the module is cythonized
                # Although python linters and typecheckers will also warn you about mismatching types
```

## IntEnum to int conversion

Similar to last example. Pure python will convert and IntEnum value to int,
cythonized code will not.

```python
from enum import IntEnum

class State(IntEnum):
    AAA = 0
    BBB = 1

def foo(a: int, b: int): ...


foo(State.AAA, 2)   # ok in pure python, TypeError in cython

```
Two ways around are possible.

### 1. Accept both int and the Enum as param types

This may be preferable if you want to restrict input values.

```python
from enum import IntEnum
from typing import Union

class State(IntEnum):
    AAA = 0
    BBB = 1


def foo(a: Union[int, State], b: int): ...

foo(State.AAA, 2)  # ok everywhere
foo(1, 2)          # still ok
```

### 2. Convert to int at the call site

In case int is more appropriate, or you can't modify the function.


```python
from enum import IntEnum

class State(IntEnum):
    AAA = 0
    BBB = 1


def foo(a: int, b: int): ...

foo(State.AAA.value, 2)     # ok everywhere
foo(State.AAA, 2)           # not ok, same as initial example.
```

## Reassign types of a variable in the same scope

In python, the following snippet is legal:

```python
def bar(msg: str): ...

def foo(value: int):
    value = str(value)     # TypeError in cython, `value` is typed as an int
    bar(value)
```

In cython, like in C and C++, it is not possible to reassign the type of variable this way.

Instead, use this:

```python

def bar(msg: str): ...

def foo(value: int):
    msg = str(value)
    bar(msg)
```
Sometimes, you may also find more appropriate names for the converted value.


# Credits

This package was created with [Cookiecutter][1] and the [audreyr/cookiecutter-pypackage][2] project template.


[1]: https://github.com/audreyr/cookiecutter

[2]: https://github.com/audreyr/cookiecutter-pypackage

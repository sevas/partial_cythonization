#!/usr/bin/env python

"""Tests for `partial_cythonization` package."""

from pathlib import Path
import sysconfig
import sys
import subprocess

from partial_cythonization import obfuscate

THIS_DIR = Path(__file__).parent
PROJECT_DIR = THIS_DIR.parent
SRC_PKG_DIR = PROJECT_DIR / "project_to_obfuscate" / "some_package"


def test_partial_cythonization_only_compiles_marked_files(tmp_path):
    ext_suffix = sysconfig.get_config_var("EXT_SUFFIX")
    target_dir = tmp_path / "_obfuscated"
    include_data = ["*.txt", "*data/*.csv"]
    always_exclude = ["some_package/subpkg2/*"]
    obfuscate.obfuscate_package(
        src=SRC_PKG_DIR,
        dest=target_dir,
        clean=True,
        include_data=include_data,
        always_exclude=always_exclude,
    )

    expected = {
        "included": [
            f"some_package/mod2{ext_suffix}",
            "some_package/mod1.py",
            "some_package/mod3_nb.py",
            "some_package/__init__.py",
            f"some_package/subpkg/mod11{ext_suffix}",
            "some_package/subpkg/__init__.py",
            "some_package/data/file1.csv",
            "some_package/data/file3.csv",
            "some_package/version.txt",

        ],
        "excluded": [
            "some_package/subpkg/mod11.py",
            "some_package/mod2.py",
            f"some_package/mod3_nb{ext_suffix}",
            f"some_package/__init__{ext_suffix}",
            f"some_package/subpkg/__init__{ext_suffix}",
            "some_package/subpkg2/never_share.py",
            f"some_package/subpkg2/never_share{ext_suffix}",
            "some_package/subpkg2/__init__.py",
        ],
    }

    for fp in expected["included"]:
        assert (target_dir / fp).exists(), f"{fp} should be in obfuscated package"

    for fp in expected["excluded"]:
        assert not (target_dir / fp).exists(), f"{fp} should not be in obfuscated package"

    test_cmd = [sys.executable, "-m", "pytest", str(target_dir / "tests"), "--no-cov"]
    subprocess.check_call(test_cmd, cwd=target_dir)


def test_all_cythonization_compiles_all_py_files_except_the_globally_excluded_ones(tmp_path):
    ext_suffix = sysconfig.get_config_var("EXT_SUFFIX")
    target_dir = tmp_path / "_obfuscated"
    include_data = ["*.txt", "*data/*.csv"]
    always_exclude = ["some_package/subpkg2/*"]
    obfuscate.obfuscate_package(
        src=SRC_PKG_DIR,
        dest=target_dir,
        clean=True,
        compile_all=True,
        include_data=include_data,
        always_exclude=always_exclude,
    )

    expected = {
        "included": [
            f"some_package/mod2{ext_suffix}",
            f"some_package/mod1{ext_suffix}",
            "some_package/mod3_nb.py",
            "some_package/__init__.py",
            f"some_package/subpkg/mod11{ext_suffix}",
            "some_package/subpkg/__init__.py",
            "some_package/data/file1.csv",
            "some_package/data/file3.csv",
            "some_package/version.txt",

        ],
        "excluded": [
            "some_package/subpkg/mod11.py",
            "some_package/mod2.py",
            "some_package/mod1.py",
            f"some_package/mod3_nb{ext_suffix}",
            f"some_package/__init__{ext_suffix}",
            f"some_package/subpkg/__init__{ext_suffix}",
            "some_package/subpkg2/never_share.py",
            f"some_package/subpkg2/never_share{ext_suffix}",
            "some_package/subpkg2/__init__.py",
        ],
    }

    for fp in expected["included"]:
        assert (target_dir / fp).exists(), f"{fp} should be in obfuscated package"

    for fp in expected["excluded"]:
        assert not (target_dir / fp).exists(), f"{fp} should not be in obfuscated package"

    test_cmd = [sys.executable, "-m", "pytest", str(target_dir / "tests"), "--no-cov"]
    subprocess.check_call(test_cmd, cwd=target_dir)

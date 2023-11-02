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
    include_data = ["*.txt", "*.csv"]
    obfuscate.obfuscate_package(src=SRC_PKG_DIR, dest=target_dir, clean=True, include_data=include_data)

    assert (target_dir / "some_package" / "subpkg" / f"mod11{ext_suffix}").exists()
    assert (target_dir / "some_package" / f"mod2{ext_suffix}").exists()

    test_cmd = [sys.executable, "-m", "pytest", str(target_dir/"tests"), "--no-cov"]
    subprocess.check_call(test_cmd, cwd=target_dir)

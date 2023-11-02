"""Main module."""
import subprocess
import shutil
import sysconfig
import fnmatch
import logging
from pathlib import Path
from typing import List

logging.basicConfig(format="%(asctime)s %(levelname)8s %(message)s")
logger = logging.getLogger("partcy")


SETUP_PY = """
# This file was generated by partial_cythonization.
from pathlib import Path
from setuptools import setup
from Cython.Build import cythonize

THIS_DIR = Path(__file__).parent
obfuscate_list_file = Path(THIS_DIR / "_obfuscate_list.txt")

obfuscate_list = obfuscate_list_file.read_text().split("\\n")

setup(
    name='Hello world app',
    ext_modules=cythonize(obfuscate_list)
)
"""


def should_include(fp: Path, include_list: List[str]) -> bool:
    for pat in include_list:
        if fnmatch.fnmatch(fp, pat):
            return True
    return False


def should_exclude(fp: Path, exclude_list: List[str]) -> bool:
    for pat in exclude_list:
        if fnmatch.fnmatch(fp, pat):
            return True
    return False


def detect_numba_usage(txt):
    return "import numba" in txt or "from numba" in txt


def obfuscate_package(
    src: str | Path,
    dest: str | Path,
    compile_all: bool = False,
    clean: bool = False,
    include_data=None,
    always_exclude=None,
):
    """Obfuscate a python package.

    Parameters
    ----------
    src
        Path to the source package.
    dest
        Path to the destination package.
    compile_all
        Whether to compile all python files found in the source package
    clean
        Whether to clean the cythonized files from the source package after obfuscation
    """
    src = Path(src)
    dest = Path(dest)
    shutil.rmtree(dest, ignore_errors=True)
    dest.mkdir(exist_ok=True, parents=True)

    if include_data is None:
        include_data = []

    if always_exclude is None:
        always_exclude = []

    src_pkg_dir = src.parent

    included_files = []
    ignored_files = []
    numba_using_files = []

    for fp in src.rglob("*"):
        if fp.is_dir() or fp.suffix == ".pyc":
            continue

        if should_exclude(fp.relative_to(src_pkg_dir), exclude_list=always_exclude):
            continue

        elif fp.suffix == ".py":
            included_files.append(fp)
        elif should_include(fp.relative_to(src_pkg_dir), include_list=include_data):
            included_files.append(fp)
        else:
            ignored_files.append(fp)

    # no need to cythonize init.py files
    py_modules = [each for each in included_files if each.suffix == ".py" and each.name != "__init__.py"]

    # detect files using numba and remove them from the list of module to cythonize
    for each in py_modules:
        txt = each.read_text()
        if detect_numba_usage(txt):
            logger.warning(f"File {each} uses the numba jit compiler, and cannot be cythonized.")
            py_modules.remove(each)
            included_files.append(each)
            numba_using_files.append(each)

    logger.info(f"Found {len(ignored_files)} files to ignore.")
    for each in ignored_files:
        logger.debug(f"    {each}")

    logger.info("Collecting files to obfuscate...")
    to_obfuscate = []
    for mod in py_modules:
        # print(f"--- Detecting if {mod} needs to be cythonized")
        if compile_all:
            to_obfuscate.append(str(mod.relative_to(src_pkg_dir)))
        else:
            try:
                txt = mod.read_text().split("\n")
            except UnicodeDecodeError:
                txt_b = mod.read_bytes()

                txt = txt_b.decode("utf-8", "ignore")

            if txt[0].startswith("# obfuscate_with_cython: True"):
                to_obfuscate.append(str(mod.relative_to(src_pkg_dir)))
    if to_obfuscate:
        logger.info(f"Found {len(to_obfuscate)} files to obfuscate.")
        for each in to_obfuscate:
            logger.info(f"    {each}")
    else:
        logger.info("Found no files to obfuscate. Exiting.")
        return

    (src.parent / "_obfuscate_list.txt").write_text("\n".join(to_obfuscate))
    (src.parent / "setup_generated.py").write_text(SETUP_PY)

    cmd = ["python", "setup_generated.py", "build_ext", "--inplace"]
    logger.info("Running cython on selected files")
    logger.info(f"     With command: {' '.join(cmd)}")
    logger.info(f"     In directory: {src_pkg_dir.absolute()}")

    subprocess.run(cmd, cwd=str(src_pkg_dir))
    logger.info("Done.")

    logger.info("")
    logger.info("Copying package files with obfuscated modules")
    ext_suffix = sysconfig.get_config_var("EXT_SUFFIX")
    to_clean = []
    for fp in included_files:
        if str(fp.relative_to(src_pkg_dir)) in to_obfuscate:
            # copy compiled file
            matching_ext = list(fp.parent.glob(fp.stem + ext_suffix))
            if matching_ext:
                dest_fp = dest / matching_ext[0].relative_to(src_pkg_dir)
                dest_fp.parent.mkdir(exist_ok=True, parents=True)
                logger.debug(f"Copying {matching_ext[0]} to {dest_fp}")
                shutil.copy(matching_ext[0], dest_fp)
                to_clean.append(matching_ext[0])
            else:
                raise FileNotFoundError(
                    f"Could not find compiled file for {fp}. This means that cython failed to compile the file."
                )
        else:
            dest_fp = dest / fp.relative_to(src_pkg_dir)
            dest_fp.parent.mkdir(exist_ok=True, parents=True)
            logger.debug(f"Copying {fp} to {dest_fp}")
            shutil.copy(fp, dest_fp)

    shutil.copytree(src.parent / "tests", dest / "tests")

    if clean:
        logger.info("Cleaning up cythonized files")
        for each in to_clean:
            c_file_name = each.name.replace(ext_suffix, ".c")
            logger.info(f"    {each} and {c_file_name}")
            each.unlink()
            (each.parent / c_file_name).unlink()

    if numba_using_files:
        logger.warning("")
        logger.warning("The following files were not cythonized because they use numba:")
        for each in numba_using_files:
            logger.warning(f"     {each}")


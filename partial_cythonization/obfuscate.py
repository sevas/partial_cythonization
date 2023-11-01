"""Main module."""
import subprocess
import shutil
from datetime import datetime
from pathlib import Path


def obfuscate_package(src: str, dest: str):
    """Obfuscate a python package.

    Parameters
    ----------
    src
        Path to the source package.
    dest
        Path to the destination package.
    """
    src = Path(src)
    dest = Path(dest)
    shutil.rmtree(dest, ignore_errors=True)
    dest.mkdir(exist_ok=True, parents=True)

    work_dir = src.parent.parent
    src_pkg_dir = src.parent

    all_modules = []

    for fp in src.rglob("*.py"):
        all_modules.append(fp)

    print("--- Collecting files to obfuscate...")
    to_obfuscate = []
    for mod in all_modules:
        txt = mod.read_text().split("\n")
        if txt[0].startswith("# obfuscate_with_cython: True"):
            to_obfuscate.append(str(mod.relative_to(src_pkg_dir)))
    print("--- Found: ", to_obfuscate)

    print("--- Running cython on selected files...")
    with open(src.parent / f"_obfuscate_list.txt", "w") as f:
        f.write("\n".join(to_obfuscate))

    cmd = ["python", "setup_generated.py", "build_ext", "--inplace"]
    subprocess.run(cmd, cwd=str(src_pkg_dir))
    print("--- Done.")

    print("--- Copying package files with obfuscated modules")

    for fp in all_modules:
        if str(fp.relative_to(src_pkg_dir)) in to_obfuscate:
            # copy compiled file
            pattern = fp.stem + "*.so"
            matching_ext = list(fp.parent.glob(fp.stem + "*.so"))
            if matching_ext:
                dest_fp = dest / matching_ext[0].relative_to(src_pkg_dir)
                dest_fp.parent.mkdir(exist_ok=True, parents=True)
                shutil.copy(matching_ext[0], dest_fp)
            else:
                raise FileNotFoundError(f"Could not find compiled file for {fp}. This means that cython failed to compile the file.")
        else:
            dest_fp = dest / fp.relative_to(src_pkg_dir)
            dest_fp.parent.mkdir(exist_ok=True, parents=True)
            shutil.copy(fp, dest_fp)

    shutil.copytree(src.parent / "tests", dest / "tests")


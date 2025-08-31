"""Console script for partial_cythonization."""

import sys
import click
from partial_cythonization.obfuscate import obfuscate_package
import logging
import toml

logger = logging.getLogger("partcy")


@click.command()
@click.argument("src", type=click.Path(exists=True))
@click.argument("dest", type=click.Path(exists=False))
@click.option("--compile-all", "-a", is_flag=True, default=False)
@click.option("--clean", "-c", is_flag=True, default=False)
@click.option("--config", type=click.Path(exists=True))
@click.option("--log-level", "-l", type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]))
def main(src, dest, compile_all, clean, config, log_level):
    """Console script for partial_cythonization."""

    logger.setLevel(log_level or "INFO")
    cfg = toml.load(config)

    obfuscate_package(
        src,
        dest,
        compile_all=compile_all,
        clean=clean,
        include_data=cfg.get("include_data", list()),
        always_exclude=cfg.get("always_exclude", list()),
        never_obfuscate=cfg.get("never_obfuscate", list()),
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

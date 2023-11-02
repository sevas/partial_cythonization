"""Console script for partial_cythonization."""
import sys
import click
from partial_cythonization.obfuscate import obfuscate_package
import toml


@click.command()
@click.argument("src", type=click.Path(exists=True))
@click.argument("dest", type=click.Path(exists=False))
@click.option("--compile-all", "-a", is_flag=True, default=False)
@click.option("--clean", "-c", is_flag=True, default=False)
@click.option("--config", type=click.Path(exists=True))
def main(src, dest, compile_all, clean, config):
    """Console script for partial_cythonization."""

    cfg = toml.load(config)

    print(cfg)
    obfuscate_package(
        src,
        dest,
        compile_all=compile_all,
        clean=clean,
        include_data=cfg["config"]["include_data"],
        always_exclude=cfg["config"]["always_exclude"],
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

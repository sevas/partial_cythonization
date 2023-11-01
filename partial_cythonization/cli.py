"""Console script for partial_cythonization."""
import sys
import click
from partial_cythonization.obfuscate import obfuscate_package


@click.command()
@click.argument('src', type=click.Path(exists=True))
@click.argument('dest', type=click.Path(exists=False))
@click.option('--compile-all', '-a', is_flag=True, default=False)
def main(src, dest, compile_all):
    """Console script for partial_cythonization."""
    obfuscate_package(src, dest, compile_all=compile_all)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

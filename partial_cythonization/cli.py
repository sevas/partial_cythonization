"""Console script for partial_cythonization."""
import sys
import click
from partial_cythonization.obfuscate import obfuscate_package


@click.command()
@click.argument('src', type=click.Path(exists=True))
@click.argument('dest', type=click.Path(exists=False))
def main(src, dest):
    """Console script for partial_cythonization."""
    obfuscate_package(src, dest)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

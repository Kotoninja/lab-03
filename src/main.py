import sys

from scripts.v1.catalog_demo import run
from src.errors import CatalogError


def main() -> None:
    """Run the catalog demo."""
    run()


if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except CatalogError as e:
        sys.stdout.write(str(e))
        sys.exit(2)

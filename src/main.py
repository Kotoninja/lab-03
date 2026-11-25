import sys

from scripts.v1.catalog_demo import run
from src.errors import CatalogError


def main() -> None:
    """Запустить демонстрационную версию"""
    run()


if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except CatalogError as e:
        sys.stdout.write(str(e) + "\n")
        sys.exit(2)

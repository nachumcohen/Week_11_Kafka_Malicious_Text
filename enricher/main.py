from enricher import Enricher


def main():
    with Enricher() as enricher:
        enricher.enrich()


if __name__ == "__main__":
    main()
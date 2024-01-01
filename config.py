import argparse
from dataclasses import dataclass


@dataclass(frozen=True)
class Config(object):
    quiet: bool = True
    reindex: bool = False
    MAX_EVENTS_TO_SHOW = 50
    CONFIDENCE_THRESHOLD = 0.35


def _build_parser() -> argparse.ArgumentParser:
    """Builds parser object from command line arguments.
    :return: parser object.
    """
    parser = argparse.ArgumentParser(description="Zoe: Calendar management chatbot")

    parser.add_argument(
        "--reindex",
        action="store_true",
        help="loads intent_sets into memory and retrains classifier. CAUTION: this operation may be "
        "time-consuming",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="increase output verbosity (run in logging mode; by default, logs are written to console)",
    )

    return parser


def config() -> Config:
    """Parses command line arguments and returns a Config object.
    :return: Config object.
    """
    parser = _build_parser()
    args = parser.parse_args()

    return Config(quiet=not args.verbose, reindex=args.reindex)

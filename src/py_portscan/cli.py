"""Provide the CLI interface for py-portscan."""

from __future__ import annotations

import argparse
import sys
from typing import Sequence

import py_portscan.input
import py_portscan.portscan


def parse_arguments(arguments: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="A Python port scanner."
    )
    parser.add_argument(
        "targets_file",
        type=str,
        help="CSV file containing target hosts and ports to scan."
    )
    return parser.parse_args(arguments)


def validate_input_file(file_path: str) -> None:
    """Validate the input file path."""
    if file_path == "-":
        if sys.stdin is None or sys.stdin.closed:    # pylint: disable=using-constant-test
            raise argparse.ArgumentTypeError(
                "Standard input is closed. Please provide a input file."
            )
    else:
        try:
            with open(file_path, 'r', encoding='utf-8'):
                pass
        except FileNotFoundError as exception:
            raise argparse.ArgumentTypeError(
                f"Input file '{file_path}' not found.") from exception
        except IsADirectoryError as exception:
            raise argparse.ArgumentTypeError(
                f"'{file_path}' is a directory, not a file.") from exception
        except Exception as exception:
            raise argparse.ArgumentTypeError(
                f"An error occurred while accessing input file '{file_path}': {exception}"
                ) from exception


def validate_arguments(args: argparse.Namespace) -> None:
    """Validate the parsed arguments."""
    validate_input_file(args.targets_file)


def main(arguments: Sequence[str] | None = None) -> None:
    """Entry point for the py-portscan CLI tool."""
    # Set short traceback by default
    sys.tracebacklimit = 0
    if arguments is None:
        arguments = sys.argv[1:]
    parsed_arguments = parse_arguments(arguments)
    validate_arguments(parsed_arguments)

    targets = py_portscan.input.read_input_csv(parsed_arguments.targets_file)

    print(",".join(py_portscan.portscan.ScanResult.get_csv_header()))
    scan_function = py_portscan.portscan.scan_targets_parallel
    # scan_function = py_portscan.scan.scan_targets
    for result in scan_function(targets):
        print(",".join(result.to_csv_row()))


if __name__ == "__main__":
    main(sys.argv[1:])

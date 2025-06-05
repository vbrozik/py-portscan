"""Provide input data handling for py-portscan."""

from __future__ import annotations

import csv
from ipaddress import IPv4Address, IPv6Address
import sys
from contextlib import contextmanager
from typing import Iterator, NamedTuple


class ScanTarget(NamedTuple):
    """Represents a target host and port for scanning."""

    host_address: IPv4Address | IPv6Address
    """IP address of the target host."""
    port: int
    """Port number of the target host."""

    @classmethod
    def get_csv_header(cls) -> list[str]:
        """Get the CSV header for this scan target."""
        return ["host", "port"]

    def to_csv_row(self) -> list[str]:
        """Convert the scan target to a CSV row."""
        return [str(self.host_address), str(self.port)]


@contextmanager
def open_input_csv_file(file_path: str) -> Iterator[Iterator[list[str]]]:
    """Open the input CSV file or stdin and yield a CSV reader.

    Args:
        file_path: Path to the CSV file or '-' for stdin.

    Yields:
        CSV reader object for the input.
    """
    if file_path == "-":
        yield csv.reader(sys.stdin)
    else:
        with open(file_path, "r", encoding="utf-8") as file:
            yield csv.reader(file)


def read_input_csv(file_path: str) -> list[ScanTarget]:
    """Read the input CSV file and return a list of ScanTarget objects.

    Args:
        file_path: Path to the CSV file or '-' for stdin.

    Returns:
        List of ScanTarget objects containing host addresses and ports.
    """
    targets: list[ScanTarget] = []
    with open_input_csv_file(file_path) as csv_reader:
        try:
            header = next(csv_reader)
        except StopIteration as exception:
            raise ValueError(f"CSV file {file_path} is empty or malformed.") from exception
        if header != ScanTarget.get_csv_header():
            raise ValueError(f"CSV header must be {ScanTarget.get_csv_header()}.")
        for row in csv_reader:
            if len(row) != 2:
                raise ValueError(f"CSV row {row} must contain exactly two columns.")
            host_str, port_str = row
            try:
                host_address = IPv4Address(host_str) if '.' in host_str else IPv6Address(host_str)
            except ValueError as exception:
                raise ValueError(f"Invalid host address '{host_str}': {exception}") from exception
            try:
                port = int(port_str)
            except ValueError as exception:
                raise ValueError(f"Invalid port number '{port_str}': {exception}") from exception
            targets.append(ScanTarget(host_address=host_address, port=port))
    return targets

"""Scan targets."""

from __future__ import annotations

import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Iterable, Iterator, NamedTuple

from py_portscan.input import ScanTarget


class ScanResult(NamedTuple):
    target: ScanTarget
    result: str

    @classmethod
    def get_csv_header(cls) -> list[str]:
        """Get the CSV header for this scan result."""
        return ScanTarget.get_csv_header() + ["result"]

    def to_csv_row(self) -> list[str]:
        """Convert the scan result to a CSV row."""
        return self.target.to_csv_row() + [self.result]


def scan_target(target: ScanTarget) -> str:
    """Scan a single target and return the result.

    Args:
        target: A ScanTarget object containing the host address and port.

    Returns:
        A string representing the scan result.
    """
    try:
        with socket.create_connection((str(target.host_address), target.port), timeout=2):
            return "open"
    except (OSError, ValueError):
        return "closed"


def scan_targets(targets: Iterable[ScanTarget]) -> Iterator[ScanResult]:
    """Scan the provided targets and return the results.

    Args:
        targets: An iterable of ScanTarget objects.

    Yields:
        ScanResult objects containing the scan results.
    """
    for target in targets:
        result = scan_target(target)
        yield ScanResult(target=target, result=result)


def scan_targets_parallel(
        targets: Iterable[ScanTarget], max_workers: int = 20) -> Iterator[ScanResult]:
    """Scan the provided targets in parallel and return the results as they come.

    Args:
        targets: An iterable of ScanTarget objects.
        max_workers: The maximum number of threads to use.

    Yields:
        ScanResult objects containing the scan results.
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_target = {
                executor.submit(scan_target, target): target
                for target in targets}
        for future in as_completed(future_to_target):
            target = future_to_target[future]
            try:
                result = future.result()
            except Exception:   # pylint: disable=broad-except  # We want the scan to continue
                result = "error"
            yield ScanResult(target=target, result=result)

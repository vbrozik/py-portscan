"""Provide tests for the CLI entry point of py-portscan."""


from __future__ import annotations

import contextlib
import sys

from py_portscan import cli


def test_cli_help(monkeypatch, capsys) -> None:
    monkeypatch.setattr(sys, "argv", ["py-portscan", "--help"])
    with contextlib.suppress(SystemExit):
        cli.main()
    captured = capsys.readouterr()
    assert "usage" in captured.out.lower()

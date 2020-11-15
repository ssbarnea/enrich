"""Tests for rich module."""
import sys

from enrich.console import Console


def test_rich_console_ex() -> None:
    """Validate that ConsoleEx can capture output from print() calls."""
    console = Console(record=True, redirect=True)
    console.print("alpha")
    print("beta")
    sys.stdout.write("gamma\n")
    sys.stderr.write("delta\n")
    # While not supposed to happen we want to be sure that this will not raise
    # an exception. Some libraries may still sometimes send bytes to the
    # streams, notable example being click.
    sys.stdout.write(b"epsilon\n")  # type: ignore
    text = console.export_text()
    assert text == "alpha\nbeta\ngamma\ndelta\nepsilon\n"


def test_rich_console_ex_ansi() -> None:
    """Validate that ANSI sent to sys.stdout does not become garbage in record."""
    print()
    console = Console(force_terminal=True, record=True, redirect=True)
    console.print("[green]this from Console.print()[/green]", style="red")

    text = console.export_text(clear=False)
    assert "this from Console" in text

    html = console.export_html(clear=False)
    assert "#008000" in html
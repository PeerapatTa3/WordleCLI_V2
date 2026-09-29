"""Rendering helpers for Wordle tiles, the live board, and history tables.

This module only builds and prints Rich objects. It holds no game state and
does no file or network I/O, so it is easy to test with a recording Console.
"""

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class BoardRenderer:
    """Turn (word, feedback) rows into colored Wordle tiles and tables."""

    STYLES = {
        "✓": "white on green",   # correct letter, correct position
        "-": "white on yellow",  # correct letter, wrong position
    }
    DEFAULT_STYLE = "white on bright_black"  # "x": letter not in the word
    EMPTY_CHAR = "_"

    def __init__(self, console=None):
        """Use the given Rich console, or create one when none is supplied."""
        self.console = console or Console()

    @classmethod
    def tile(cls, char, feedback, padding=2):
        """Return Rich markup for one colored letter tile."""
        style = cls.STYLES.get(feedback, cls.DEFAULT_STYLE)
        pad = " " * padding
        return f"[bold {style}]{pad}{char}{pad}[/bold {style}]"

    @classmethod
    def empty_tile(cls, padding=2):
        """Return Rich markup for a not-yet-used board cell."""
        pad = " " * padding
        return f"[dim white]{pad}{cls.EMPTY_CHAR}{pad}[/dim white]"

    def build_table(self, rows, word_length=5, max_attempts=None, compact=False):
        """Build a Rich table from ``rows`` of ``(word, feedback)`` pairs.

        When ``max_attempts`` is given, unused rows are filled with empty
        tiles (live board). ``compact=True`` uses narrower tiles (history).
        """
        padding = 1 if compact else 2
        min_width = 3 if compact else 5

        table = Table(
            show_header=False,
            show_lines=True,
            box=box.ROUNDED,
            padding=(0, padding),
        )
        for _ in range(word_length):
            table.add_column(justify="center", min_width=min_width)

        for word, feedback in rows:
            table.add_row(*(self.tile(char, fb, padding) for char, fb in zip(word, feedback)))

        if max_attempts is not None:
            for _ in range(max_attempts - len(rows)):
                table.add_row(*[self.empty_tile(padding)] * word_length)

        return table

    def build_history_table(self, rows, word_length=5):
        """Build the compact table used for one finished game in history."""
        return self.build_table(rows, word_length, compact=True)

    def render_board(self, rows, max_attempts=6, word_length=5):
        """Print the live game board inside a titled panel."""
        table = self.build_table(rows, word_length, max_attempts)
        self.console.print(
            Panel(table, title="[bold cyan]WORDLE BOARD[/bold cyan]", expand=False)
        )
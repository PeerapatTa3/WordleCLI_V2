from rich.console import Console
from src.board_renderer import BoardRenderer


def test_tile_colors():
    assert "on green" in BoardRenderer.tile("A", "✓")
    assert "on yellow" in BoardRenderer.tile("A", "-")
    assert "on bright_black" in BoardRenderer.tile("A", "x")


def test_board_pads_unused_rows():
    r = BoardRenderer(Console(record=True, width=60))
    table = r.build_table([("CRANE", ["✓", "-", "x", "x", "x"])], 5, max_attempts=6)
    assert table.row_count == 6

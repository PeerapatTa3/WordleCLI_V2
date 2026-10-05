from src.history_manager import calculate_stats, group_history_by_game


def test_empty_history_has_no_groups_or_statistics():
    assert group_history_by_game([]) == {}
    assert calculate_stats([]) is None


def test_legacy_records_without_game_numbers_form_one_game():
    history = [
        {"guess": "CRANE", "correct": False, "attempt": 1},
        {"guess": "GRAPE", "correct": True, "attempt": 2},
    ]

    assert group_history_by_game(history) == {1: history}
    stats = calculate_stats(history)
    assert stats["total_games"] == 1
    assert stats["win_count"] == 1
    assert stats["distribution"][2] == 1


def test_statistics_reset_streak_after_loss_and_count_win_distribution():
    history = [
        {"game_number": 1, "correct": True, "attempt": 2},
        {"game_number": 2, "correct": False, "attempt": 6},
        {"game_number": 3, "correct": True, "attempt": 4},
        {"game_number": 4, "correct": True, "attempt": 2},
    ]

    stats = calculate_stats(history)

    assert stats["total_games"] == 4
    assert stats["win_count"] == 3
    assert stats["win_rate"] == 75
    assert stats["current_streak"] == 2
    assert stats["distribution"] == {1: 0, 2: 2, 3: 0, 4: 1, 5: 0, 6: 0}

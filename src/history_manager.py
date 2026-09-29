"""History and statistics calculation logic."""

def group_history_by_game(history):
    """Group flat history records into a dictionary keyed by game number."""
    if not history:
        return {}

    grouped = {}
    has_game_numbers = any("game_number" in record for record in history)

    if has_game_numbers:
        for record in history:
            game_number = record.get("game_number", 1)
            grouped.setdefault(game_number, []).append(record)
    else:
        grouped[1] = history

    return grouped


def calculate_stats(history):
    """Compute aggregate game statistics from history records.

    Returns a dict containing:
      - total_games
      - win_count
      - win_rate
      - current_streak
      - distribution (dict mapping attempt_number -> count)
    """
    grouped_games = group_history_by_game(history)
    if not grouped_games:
        return None

    games = [grouped_games[key] for key in sorted(grouped_games)]
    wins = [any(record.get("correct", False) for record in game) for game in games]
    
    total_games = len(games)
    win_count = sum(wins)
    win_rate = (win_count / total_games * 100) if total_games > 0 else 0.0

    current_streak = 0
    for won in reversed(wins):
        if not won:
            break
        current_streak += 1

    distribution = {
        attempt: sum(
            1 for game in games
            if any(record.get("correct") and record.get("attempt") == attempt for record in game)
        )
        for attempt in range(1, 7)
    }

    return {
        "total_games": total_games,
        "win_count": win_count,
        "win_rate": win_rate,
        "current_streak": current_streak,
        "distribution": distribution,
    }


def search_history(history, keyword):
    """Search guess_history by matching a keyword in guess strings."""
    keyword = (keyword or "").strip().upper()
    if not keyword:
        return history

    return [item for item in history if keyword in str(item.get("guess", "")).upper()]


def filter_history(history, condition):
    """Filter history by a given condition such as correct guesses."""
    if condition == "correct":
        return [item for item in history if bool(item.get("correct"))]
    if condition == "incorrect":
        return [item for item in history if not bool(item.get("correct"))]
    return history
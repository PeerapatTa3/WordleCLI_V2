# Sprint 3 To-Do — WordleCLI_V2

Two changes: (A) offline-first local dictionary, (B) in-place redraw for a cleaner CLI.

> **Status (checked against the current `cli.py`, 2026-09-29).** Items that live in files I could not see
> (`word_bank.py`, `word_api.py`, `scripts/`, `tests/`, docs) are left unchecked until verified.

## A. Local dictionary (no network at runtime)

**Problem:** every game start makes 2 Datamuse calls (5s timeout each) and unknown guesses hit the Dictionary API (3-10s). `fetch_word_pool()` can loop forever when the API is down. `Path("data/...")` is CWD-relative.

- [ ] `scripts/build_wordlists.py` (one-time; API code may live here): filter a public-domain list (e.g. ENABLE) to 5-letter alpha words, uppercase, sorted, deduped.
  - `data/valid_words.txt` (~9-13k) and `data/answers.txt` (~1-3k most frequent; drop plurals, proper nouns, offensive words). Commit both.
- [ ] `src/word_bank.py`: `load_word_bank(length=5)` returns `(answers tuple, valid_words frozenset)`.
  - Paths from `Path(__file__)`; force `valid = valid | answers`; missing/empty file → `DEFAULT_WORD_POOL`.
  - *Caller in `cli.py` already uses this contract; verify the module itself.*
- [x] `cli.py`
  - [x] `play_game()`: load bank once via `load_word_bank(5)`, pick with `random.choice(answers)`; `fetch_random_word` / `fetch_valid_words` removed.
  - [x] `get_secret_word()`: no API; keeps `WORDLE_TEST_WORD`; `play_game()` adds the secret to `valid_words` (`valid_words | {secret_word}`), so the test word is always a legal guess.
  - [x] `get_guess_input()`: validates locally with `guess.upper() in valid_words`; `word_validator` arg and "might take a while" spinner removed.
  - [x] `is_valid_guess()`: checks membership directly, no per-call set rebuild.
- [ ] `word_api.py`: move to `scripts/` or off the runtime path; delete `is_valid_dictionary_word`, `DICTIONARY_RETRIES`, `DICTIONARY_CACHE`; fix unreachable `return None` and the `fetch_word_pool` infinite loop.
  - [x] `cli.py` no longer imports `word_api` or `requests`.
- [ ] Retire `data/word_pool.json` (or keep only as fallback). `history.json` unchanged.

## B. In-place redraw

**Problem:** each guess prints a new board panel, the typed guess stays on screen, and each invalid guess adds another error panel.

- [x] Helpers in `cli.py`: `erase_lines(n)` (write `"\033[F\033[K" * n`, flush) and `clear_screen()` (`console.clear()`); both no-ops when `not console.is_terminal`.
- [x] `render_game_screen(board_history, attempt, max_attempts, word_length, message=None)`: clear, print `Attempt x/6` header, board (reuse `_render_wordle_board`), optional one-line message.
  - [ ] Use it for hint output too (see F1: hint text is currently wiped by the next redraw).
  - [x] `answer` output: printed after the last redraw, then the round ends.
- [x] `play_game()`: renders the empty board before the first prompt; redraws after each valid guess; the extra `Attempt x/6` print is gone.
- [ ] `get_guess_input()` (keep signature):
  - [x] valid → `erase_lines(1)`
  - [x] invalid → single red line containing "Invalid guess" (no Panel)
  - [ ] retry after an invalid guess → `erase_lines(2)` so the previous error is replaced. **Currently `erase_lines(1)` only, so consecutive errors stack** (see F2).
- [x] Menu/other screens: took the smaller option: redraw is limited to gameplay; History/Statistics/How to Play print below the menu without clearing.

## C. Tests

- [ ] Update `tests/test_cli.py` (it monkeypatches `cli.fetch_valid_words`, which no longer exists; old panel/board assertions).
- [ ] New: game works with no network; missing/empty word file → default list; `answers ⊆ valid_words`; `WORDLE_TEST_WORD` accepted as a guess; no `requests` call during validation.
- [ ] New: `erase_lines` / `clear_screen` write nothing when not a terminal; invalid guess prints one "Invalid guess" line.
- [ ] New: `hint` keeps its message visible; `answer` handling (see F1, F3).
- [ ] Move/trim `tests/test_word_api.py` to match where API code ends up.

## D. Manual checks

- [ ] Full game: one board on screen, no leftover typed guesses.
- [ ] 3 invalid guesses in a row: error line replaces itself (blocked by F2).
- [ ] `hint` and `answer` mid-game: no crash, board not duplicated, hint text visible (blocked by F1).
- [ ] Network off: starts and validates instantly.
- [ ] Windows Terminal + one Unix terminal; `pytest`; output redirected to a file (no stray escape codes).

## E. Docs

- [x] PLAN.md Sprint 3: dropped `api_cache.json` / `refresh_from_api`; API is a build script only; UX redraw item added.
- [x] PLAN.md Sprint Final refactor note: per-guess API validation (3-10s, network-dependent) → local set lookup; class-extraction candidates added.
- [ ] README, CHANGELOG, Wow!/Whoops! ("stacked boards and error panels → in-place redraw").

## F. Follow-ups found in code review

- [ ] **F1. `hint` message is erased immediately.** `play_game()` prints the hint, then `continue` re-enters the loop and `render_game_screen()` clears the screen. Pass the hint as `message=` to `render_game_screen()` (or skip the clear on the next pass).
- [ ] **F2. Invalid-guess errors stack.** Track whether an error line is currently shown and call `erase_lines(2)` on retry, `erase_lines(1)` otherwise.
- [ ] **F3. `answer` leaves an unfinished game.** Guesses are saved per attempt, but `answer` returns without any "lost/gave up" marker, so `display_history()` shows a game with no final record and can mislabel it. Decide: record it as a loss, or discard that game's records.
- [ ] **F4. `HISTORY_PATH = Path("data/history.json")` is still CWD-relative.** Resolve from `Path(__file__)` (required for the Sprint Final `wordle` global command).
- [ ] **F5. Dead code:** delete `colorize_feedback()` and the `colorama` import/`init()`.
- [ ] **F6. Magic numbers:** `6` (max attempts) appears 5 times and `5` is hardcoded in `get_secret_word()` / `display_how_to_play()`. Introduce `MAX_ATTEMPTS` and `WORD_LENGTH`.
- [ ] **F7. Tile coloring is duplicated** in `_render_wordle_board` and `display_history` (only padding differs). Extract a shared renderer (see Extra).

## Extra

- [x] Extracted `history_manager` from `cli.py` for Single Responsibility (`calculate_stats` now lives there).
- [ ] Candidate class extractions from `cli.py` (do in this order):
  1. `BoardRenderer`: shared tile/table building for the board, history, and (optionally) the How to Play legend. (Done)
  2. `HistoryRepository`: wraps `HISTORY_PATH`, `load_data`/`save_data`, `_next_game_number`, and grouping by game.
  3. `GameSession`: attempt counter, board history, revealed hint positions, and record building out of `play_game()`.
  4. `ConsoleUI`: wraps `console`, `display_*`, and input helpers so a fake console can be injected in tests.

## Definition of Done

- [ ] Game starts and validates with the network off, with no visible delay. *(cli.py side done; confirm `word_bank.py` and manual test.)*
- [x] No `requests` calls during gameplay (`cli.py` has no network imports).
- [ ] One board visible at a time; typed guess line doesn't remain; invalid guesses replace the previous error. *(board and typed line done; error replacement blocked by F2.)*
- [x] No escape codes or clears when output is not a terminal (`erase_lines` / `clear_screen` are guarded by `console.is_terminal`).
- [ ] `pytest` passes.
# Sprint 3 To-Do — WordleCLI_V2

Two changes: (A) offline-first local dictionary, (B) in-place redraw for a cleaner CLI.

> **Status (checked against the full repo and a `pytest` run, 2026-09-29):** 72 tests, 71 pass, 1 fails
> (`test_hint_message_is_passed_to_next_redraw`, see F1). Manual terminal checks (section D) are not verified yet.

## A. Local dictionary (no network at runtime)

**Problem:** every game start makes 2 Datamuse calls (5s timeout each) and unknown guesses hit the Dictionary API (3-10s). `fetch_word_pool()` can loop forever when the API is down. `Path("data/...")` is CWD-relative.

- [x] `scripts/build_wordlists.py` (one-time): filter a public-domain list (e.g. ENABLE) to 5-letter alpha words, uppercase, sorted, deduped.
  - `data/valid_words.txt` (8,636 words) and `data/answers.txt` (1,984 words) are committed; `answers ⊆ valid_words` holds.
- [x] `src/word_bank.py`: `load_word_bank(length=5)` returns `(answers tuple, valid_words frozenset)`.
  - Paths from `Path(__file__)`; force `valid = valid | answers`; missing/empty file → `DEFAULT_WORD_POOL`.
  - Verified by `tests/test_word_bank.py` (13 tests).
- [x] `cli.py`
  - [x] `play_game()`: load bank once via `load_word_bank(5)`, pick with `random.choice(answers)`; `fetch_random_word` / `fetch_valid_words` removed.
  - [x] `get_secret_word()`: no API; keeps `WORDLE_TEST_WORD`; `play_game()` adds the secret to `valid_words` (`valid_words | {secret_word}`), so the test word is always a legal guess.
  - [x] `get_guess_input()`: validates locally with `guess.upper() in valid_words`; `word_validator` arg and "might take a while" spinner removed.
  - [x] `is_valid_guess()`: checks membership directly, no per-call set rebuild.
- [x] `word_api.py`: Datamuse helpers moved to `scripts/word_api.py`; `is_valid_dictionary_word`, `DICTIONARY_RETRIES`, `DICTIONARY_CACHE`, `fetch_word_pool` removed. `src/word_api.py` is now only `today_word()` (NYT daily answer), not used at runtime.
  - [x] `cli.py` no longer imports `word_api` or `requests`.
- [x] Retire `data/word_pool.json` (file is gone; fallback is `DEFAULT_WORD_POOL` in `word_bank.py`). `history.json` unchanged.

## B. In-place redraw

**Problem:** each guess prints a new board panel, the typed guess stays on screen, and each invalid guess adds another error panel.

- [x] Helpers in `cli.py`: `erase_lines(n)` (write `"\033[F\033[K" * n`, flush) and `clear_screen()` (`console.clear()`); both no-ops when `not console.is_terminal`.
- [x] `render_game_screen(board_history, attempt, max_attempts, word_length, message=None)`: clear, print `Attempt x/6` header, board (reuse `_render_wordle_board`), optional one-line message.
  - [x] Hint output: solved differently from the original idea. `play_game()` prints the hint under the board without redrawing and adds 1 to `_last_render_lines`, so the hint stays visible and the next redraw erases it with the board (see F1).
  - [x] `answer` output: printed after the last redraw, then the round ends.
- [x] `play_game()`: renders the empty board before the first prompt; redraws after each valid guess; the extra `Attempt x/6` print is gone.
- [x] `get_guess_input()` (keep signature):
  - [x] valid → `erase_lines(1)`
  - [x] invalid → single red line containing "Invalid guess" (no Panel)
  - [x] retry after an invalid guess → erases the typed rows plus the previous error line, so consecutive errors no longer stack (see F2).
- [x] Menu/other screens: took the smaller option: redraw is limited to gameplay; History/Statistics/How to Play print below the menu without clearing.

## C. Tests

- [x] Update `tests/test_cli.py` (20 tests, all pass; no reference to `fetch_valid_words`).
- [x] New: game works with no network (`test_load_word_bank_makes_no_network_calls`); missing/empty word file → default list; `answers ⊆ valid_words`; `WORDLE_TEST_WORD` accepted as a guess. `cli.py` imports no network library, so guess validation cannot call `requests`.
- [x] New: `erase_lines` / `clear_screen` write nothing when not a terminal; invalid guess prints one "Invalid guess" line; consecutive errors erase `[1, 2, 2]` lines.
- [ ] `hint` keeps its message visible: test exists but **fails** (`test_hint_message_is_passed_to_next_redraw` expects the hint via `message=`, code prints it directly). `answer` handling is covered and passes (see F3).
- [x] `tests/test_word_api.py` now targets `scripts.word_api`; `tests/test_today_word.py` covers `src.word_api.today_word`.

## D. Manual checks

- [ ] Full game: one board on screen, no leftover typed guesses.
- [ ] 3 invalid guesses in a row: error line replaces itself.
- [ ] `hint` and `answer` mid-game: no crash, board not duplicated, hint text visible.
- [ ] Network off: starts and validates instantly.
- [ ] Windows Terminal + one Unix terminal; `pytest`; output redirected to a file (no stray escape codes).

## E. Docs

- [x] PLAN.md Sprint 3: dropped `api_cache.json` / `refresh_from_api`; API is a build script only; UX redraw item added.
- [x] PLAN.md Sprint Final refactor note: per-guess API validation (3-10s, network-dependent) → local set lookup; class-extraction candidates added.
- [x] README, CHANGELOG, QA_REPORT, LEARNINGLOG, test docs, `Sprints/Sprint3.md` updated. Wow!/Whoops!: "stacked boards and error panels → in-place redraw".

## F. Follow-ups found in code review

- [x] **F1. `hint` message is erased immediately.** Fixed in the code: the hint is printed under the board, the loop skips the redraw (`needs_render = False`) and the extra line is counted. **Open:** `tests/test_sprint3.py::test_hint_message_is_passed_to_next_redraw` still asserts the older design (hint passed as `message=`) and fails. Either rewrite that test to check the printed hint / `_last_render_lines`, or change `play_game()` to pass the message.
- [x] **F2. Invalid-guess errors stack.** `get_guess_input()` tracks `error_shown` and erases the typed rows (including wrapped long input) plus the old error line.
- [x] **F3. `answer` leaves an unfinished game.** Decided: discard the game's records (`_discard_game`). Tested by `test_answer_discards_partial_game` and `test_answer_before_any_guess_writes_nothing`.
- [x] **F4. `HISTORY_PATH`** now resolves from `Path(__file__)` (`test_history_path_is_not_cwd_relative`).
- [x] **F5. Dead code:** `colorize_feedback()` and the `colorama` import/`init()` are gone from the code. **Leftover:** `colorama` is still listed in `requirements.txt`; remove that line.
- [x] **F6. Magic numbers:** `6` (max attempts) appears 5 times and `5` is hardcoded in `get_secret_word()` / `display_how_to_play()`. Introduce `MAX_ATTEMPTS` and `WORD_LENGTH`.
- [x] **F7. Tile coloring is duplicated** in `_render_wordle_board` and `display_history` (only padding differs). Extract a shared renderer (see Extra).

## Extra

- [x] Extracted `history_manager` from `cli.py` for Single Responsibility (`calculate_stats` now lives there).
- [ ] Candidate class extractions from `cli.py` (do in this order; 2-4 are candidates for the Sprint Final refactor write-up):
  1. `BoardRenderer`: shared tile/table building for the board, history, and (optionally) the How to Play legend. (Done)
  2. `HistoryRepository`: wraps `HISTORY_PATH`, `load_data`/`save_data`, `_next_game_number`, and grouping by game.
  3. `GameSession`: attempt counter, board history, revealed hint positions, and record building out of `play_game()`.
  4. `ConsoleUI`: wraps `console`, `display_*`, and input helpers so a fake console can be injected in tests.

## Definition of Done

- [x] Game starts and validates with the network off, with no visible delay. *(`word_bank.py` and `cli.py` verified by tests; a manual run offline is still worth doing.)*
- [x] No `requests` calls during gameplay (`cli.py` has no network imports).
- [x] One board visible at a time; typed guess line doesn't remain; invalid guesses replace the previous error. *(logic done and unit-tested; confirm visually, see D.)*
- [x] No escape codes or clears when output is not a terminal (`erase_lines` / `clear_screen` are guarded by `console.is_terminal`).
- [ ] `pytest` passes. *(71 of 72; the failing test is described in F1.)*
# Sprint 4 (Sprint Final) To-Do — WordleCLI_V2

Sprint Final = DevOps, CI/CD & AI Integration (see `PLAN.md`, "Sprint Final"). Roles are not rotated this sprint; the team splits work by expertise.

Five workstreams: (A) cleanup of known leftovers, (B) tests + coverage + lint, (C) CI/CD on GitHub Actions, (D) global `wordle` / `wordle start` command, (E) AI/automation feature. Then (F) manual checks carried over from Sprint 3, (G) refactor write-up, (H) docs and presentation.

> **Status (2026-10-02):** Sprint Final not started. Baseline from `tests/TEST_PLAN.md`: 72 tests, 72 pass (last recorded run 2026-09-29; re-run before starting).
> No `pyproject.toml`, no `.github/workflows/`, no coverage tooling, and no AI feature exist in the repo yet.

## Suggested order

1. A (cleanup) → 2. B (measure coverage and lint baseline) → 3. C (CI) → 4. D (packaging) → 5. E (AI feature) → 6. F (manual checks) → 7. G/H (docs, slides, demo).
CI comes before the feature work so every later change is checked automatically.

---

## A. Cleanup of known leftovers (small, do first)

**Problem:** these are listed as "Known issues" in `CHANGELOG.md` / `QA_REPORT.md` and will show up in lint, coverage and the final presentation.

- [x] Remove `colorama` from `requirements.txt` (no code imports it).
- [x ] De-duplicate `search_history` / `filter_history`: they exist in both `src/game_logic.py` and `src/history_manager.py`.
  - Keep them in `history_manager.py` (history logic lives there); update the import in `tests/test_logic.py`.
  - Decide whether `game_logic.py` re-exports them or drops them, and document the choice.
- [x] `display_history()` in `src/cli.py` re-implements the grouping that `history_manager.group_history_by_game()` already does. Replace it with the shared function.
- [ ] Audit `data/answers.txt` for words that are poor answers (names and places such as `DONNA`, `TERRY`, `JESSE`, `ALAMO`, `SODOM`; slang). The denylists in `scripts/build_wordlists.py` are tiny. Add words to the denylist, regenerate with `scripts/build_wordlists.py`, and keep `answers ⊆ valid_words` (covered by `test_real_word_bank_loads_and_is_consistent`).
- [ ] Fix stale text in docs: `PLAN.md` Sprint 3 DoD still says "71 of 72", and `README.md` roadmap says Sprint 3 has "1 test + manual check" remaining. `PRESENTATION_SLIDE_PROMPTS.md` part 5 says 28 test cases (now 72+).

## B. Tests, coverage, lint

**Goal (PLAN DoD):** unit tests cover at least 80% of the important Business/Data layer cases (normal + edge).

- [x] Add dev tooling: `pytest-cov`, `flake8` in the `dev` extra in `pyproject.toml`.
- [x] Add `.flake8` config with `max-line-length=120` and exclude `.venv`, `build`, `dist`. Root `cli.py` already uses `# noqa` for the star import.
- [x] Run and record baseline checks in `QA_REPORT.md`, then record final results.
- [x] Fix all Flake8 findings without suppressions.
- [x] Close the obvious coverage gaps:
  - [x] Add `tests/test_history_manager.py` for empty history, legacy records, streak reset, and distribution counts.
  - [x] Cover `main()` choices `1`-`5`, invalid option, and exit.
  - [x] Cover the six-guess `play_game()` loss path.
  - [x] Cover invalid `WORDLE_TEST_WORD` fallback and warning.
  - [x] Cover `data_manager.save_data()` failure paths.
  - [x] Cover `display_welcome_message()` and empty `display_history()`.
- [x] Enforce the 80% coverage target in CI and record the final 93.46% result.

## C. CI/CD with GitHub Actions

**Goal (PLAN DoD):** CI runs automatically on PRs and blocks merging when tests fail.

- [x] Create `.github/workflows/ci.yml`:
  - Triggers: `push` and `pull_request`.
  - Matrix: Python 3.12 and 3.13 (the versions already tested by the team); consider `ubuntu-latest` + `windows-latest`, since the team develops on Windows and the UI uses `✓` and Rich ANSI output.
  - Steps: checkout → `actions/setup-python` (with pip cache) → install (`pip install -e ".[dev]"` once packaging exists, otherwise `pip install -r requirements.txt flake8 pytest-cov`) → `flake8` → `pytest --cov=src --cov-fail-under=80`.
- [x] Make sure the test suite is network-free in CI (`test_load_word_bank_makes_no_network_calls`; API requests are mocked).
- [x] Confirm tests use temporary history paths; removed the obsolete tracked `data/history.json` so CI cannot depend on local gameplay data.
- [ ] Repo settings (manual, GitHub UI): branch protection on `main` → require the CI check to pass before merging.
- [x] Add a CI status badge to `README.md`.
- [ ] Prove it works for the demo: open a PR with one deliberately failing test, screenshot the red check blocking the merge, then fix it.

## D. Global `wordle` command and `wordle start`

**Goal:** `wordle` runs from any directory after `pip install`; `wordle start` skips the banner and menu and starts a game immediately.

**Packaging decisions:**
- `src/data/` is the packaged source for the word lists. The root `data/` copies are retained for now.
- The package remains named `src`; this is functional but generic and could collide with another package.
- History is stored outside the package at `~/.wordle/history.json` (Windows: `%USERPROFILE%\.wordle\history.json`), with `WORDLE_HISTORY_PATH` as an override.

Tasks:
- [x] Decide the data layout and write the decision down (this is also material for G):
  -(Selected) Option 1: use `src/data/` as the package-data location. Update `word_bank.py`, `scripts/build_wordlists.py` default output, and `tests/test_word_bank.py` (its `fake_data` fixture expects `tmp_path/src/data`).
  - Option 2: keep `data/` and install only in editable mode (`pip install -e .`). Simpler, but then "global install" works only from a clone.
- [x] Move history to a per-user location with an env var override. `HISTORY_PATH` is absolute; `tests/test_sprint3.py` continues patching `dm.HISTORY_PATH`.
- [x] Add `pyproject.toml`:
  - `[project]`: name, version, `requires-python`, `dependencies = ["rich"]` (the game does not import `requests`; it is needed only by `src/word_api.py` and `scripts/`, so put it in an extra or `dev`).
  - `[project.scripts]`: `wordle = "src.cli:main"`.
  - Hatchling package discovery includes `src`; package-local word lists are included and the history snapshot is excluded.
- [x] Add `argparse` to the entry point: `wordle` (no args) behaves as today; `wordle start` calls `play_game()` directly, with no banner or menu. `main()` accepts optional `argv=None` for tests.
  - In `start` mode, exit after the game ends; this behavior is documented in the README.
- [x] Tests: `main(["start"])` calls `play_game` and not `display_menu`; `main([])` shows the menu; unknown subcommand exits with a usage message; `--help` works.
- [x] Verify in a clean virtualenv: non-editable `pip install .`, run from an unrelated directory, load the real word lists, and save history using the per-user path/override.
- [x] `.gitignore` already excludes build artifacts and history JSON; the per-user history is outside the repository.

## E. AI / automation feature

**Constraint:** the project is offline-first (Sprint 3). Prefer a feature that needs no network and stays deterministic and testable. An LLM or API call would reintroduce the problems removed in Sprint 3 (latency, outages), so treat that as optional and out of the core scope.

**Proposal: Smart assistant (local, rule-based) with two parts**

1. **`suggest` command during play** (like `hint`: does not consume an attempt).
   - Computes the answers still consistent with every guess so far and recommends the best next guess.
   - Consistency check reuses existing logic: a candidate `w` is possible if `calculate_feedback(g, w) == fb` for every `(g, fb)` already on the board.
   - Ranking: score each candidate by letter frequency across the remaining candidates (count each letter once per word); tie-break alphabetically so results are deterministic. First suggestion with an empty board = best opening word.
   - Shows e.g. `Suggestion: CRANE (47 possible words left)`. Do not reveal the secret; only use feedback the player has already seen.
- [ ] New module `src/ai_assistant.py` in the Business Logic layer (no `print()` / `input()`):
  - [ ] `remaining_candidates(words, board_history)` → list of words consistent with all feedback.
  - [ ] `score_words(candidates)` / `suggest_guess(words, board_history)` → `(word, remaining_count)`.
  - [ ] Decide the candidate pool: `answers` for suggestions (smaller, more accurate) while still accepting any `valid_words` guess.
- [ ] Wire `suggest` into `get_guess_input()` (add to the command set `{"hint", "answer", "suggest"}`) and `play_game()`:
  - Print the result under the board without redrawing, and add the number of printed lines to `_last_render_lines` (same mechanism as `hint`, F1 in Sprint 3). Because the message may span more than one line, count lines rather than adding a flat `1`.
  - Update `display_how_to_play()` and the README "how to play" section.
- [ ] Decide whether a guess made after `suggest` is flagged in history (probably not; keep the record schema unchanged so `load_data` / stats stay compatible).

2. **Play insights** inside *View Statistics* (so the menu stays 1-5).
- [ ] `analyze_history(history)` in `ai_assistant.py` (or `history_manager.py`): average attempts on wins, most-used opening word, most frequently guessed words, letters most often marked `x` / `✓`, and a suggested opener based on the player's own results.
- [ ] Render as an extra Rich panel under the existing statistics; show nothing extra when history is empty.

**Tests for E** (new `tests/test_ai_assistant.py`):
- [ ] Empty board → all answers are candidates; suggestion is a valid word.
- [ ] After a guess with feedback, candidates shrink and always include the true secret (property check over a sample of real answers: for random secret/guess pairs, `secret in remaining_candidates(...)`).
- [ ] Duplicate-letter feedback (`ALLEY` vs `APPLE`) keeps the correct candidates.
- [ ] One candidate left → suggestion is that word; zero candidates (inconsistent input) → returns `None`, no crash.
- [ ] `suggest` in `play_game()` does not consume an attempt and does not write history (same style as the hint tests).
- [ ] `analyze_history` with empty, legacy (no `game_number`), and normal history.
- [ ] Optional: simulate N games with the assistant and assert the average solve attempts is under a threshold (also good demo evidence).

**Optional stretch (only if time):** auto-play mode (`wordle solve` / a benchmark script) that plays the assistant against all answers and reports win rate and average guesses. Good for the live demo; keep it in `scripts/`.

## F. Manual checks (carried over from Sprint 3, section D)

Still not verified, and they are open boxes in `QA_REPORT.md`, `Sprint3.md` and `Sprint3_todo.md`.

- [ ] Full game: one board on screen, no leftover typed guesses.
- [ ] 3 invalid guesses in a row: error line replaces itself (also with a long input that wraps).
- [ ] `hint`, `answer`, and the new `suggest` mid-game: no crash, board not duplicated, message visible.
- [ ] Network off: starts and validates instantly.
- [ ] Windows Terminal and one Unix terminal.
- [ ] Output redirected to a file: no stray escape codes (`python game.py > out.txt` with scripted input).
- [ ] After packaging: `wordle` and `wordle start` from an unrelated directory (see D).
- [ ] Record results (terminal, OS, Python version, pass/fail) in `QA_REPORT.md`.

## G. Refactor / technical-problems write-up

PLAN deliverable: a short document comparing the alternatives that were considered with what was actually built.

- [ ] Create `REFACTOR_NOTES.md` (or a `Sprints/Sprint4.md` section) covering:
  - [ ] Per-guess API validation (3-10 s, needs network, could hang) vs. local `frozenset` lookup (instant, offline). Include the measured difference and the tests that prove no network use.
  - [ ] Single-file CLI vs. layered modules (`cli` / `board_renderer` / `game_logic` / `history_manager` / `data_manager` / `word_bank`).
  - [ ] Class-extraction candidates not yet done (from `Sprint3_todo.md` "Extra"): `HistoryRepository`, `GameSession`, `ConsoleUI`. For each: what it would own, what it would simplify in `cli.py`, and why it was or was not done.
  - [ ] The packaging/data-layout decision from D and the history-location decision.
- [ ] Optional: actually extract one class (best value is `HistoryRepository`: wraps `HISTORY_PATH`, `load_data` / `save_data`, `_next_game_number`, `_discard_game`, `_persist`). Only do it if it is covered by existing tests and CI is green before and after.
- [ ] Short list of technical problems met in Sprints 1-3 with the fix for each (stacked boards/errors, stale in-memory history, CWD-relative paths, API latency, hint redraw test).

## H. Docs and presentation

- [ ] `CHANGELOG.md`: replace the `[v....] - Sprint Final` placeholder with a real version (e.g. `v1.0.0`); fold the `[Unreleased]` Rich-UI section into a released version; list Added / Changed / Removed / Fixed.
- [ ] `README.md`: status, features (`suggest`, insights), install via `pip install .`, `wordle` / `wordle start`, CI badge, updated architecture tree (`ai_assistant.py`, `pyproject.toml`, `.github/`), updated test counts.
- [ ] `PLAN.md`: tick the Sprint Final DoD boxes; fix the stale Sprint 3 line (see A).
- [ ] `tests/TEST_PLAN.md` and `tests/TEST_CASES.md`: add Sprint Final cases (new IDs after `S3-T28` / `TC-25`), update the test-file table and the total, add the new run command with `--cov`.
- [ ] `QA_REPORT.md`: Sprint Final section (CI evidence, coverage before/after, manual-check results).
- [ ] `LEARNINGLOG.md`: add Prompts 20+ for this sprint. The team must fill in the real prompts used (same note as Sprint 3, Prompts 17-19).
- [ ] `Sprints/Sprint4.md`: summary in the same format as `Sprints/Sprint3.md` (status, scope, verified results, Wow!/Whoops!, deliverable status, role self-assessment tables left for the team).
- [ ] `PRESENTATION_SLIDE_PROMPTS.md`: rewrite part 5 (CI/CD pipeline demo, AI feature, global command, future work) and fix the "28 tests" line; update the Canva slides to match.
- [ ] Final self-assessment tables in `README.md` (Sprint Final scores) are for the team to fill in.

### Demo checklist (5 rubric parts, from PLAN.md)

1. Problem, architecture, UML class diagram.
2. Tech stack, Python version, libraries, design principles.
3. Live demo of every function (play, history, statistics, how to play, hint, answer, suggest) plus search/filter and error cases.
4. Technical problems found and the comparison of alternatives.
5. CI/CD run on GitHub Actions, the AI feature, `wordle` / `wordle start` from another directory, and future work.

---

## Definition of Done

- [ ] Unit tests cover the Business/Data layers with ≥ 80% coverage on important cases; coverage number recorded.
- [ ] CI runs on every push/PR (lint + tests + coverage) and blocks merging when it fails.
- [ ] AI feature works offline, is covered by tests, and can be demoed live.
- [ ] `wordle` runs from any directory after `pip install`; data paths do not depend on the CWD; real word list is loaded (not the default pool).
- [ ] `wordle start` begins a game immediately with no banner/menu; plain `wordle` behaves as before.
- [ ] Manual terminal checks (section F) completed and recorded.
- [ ] Technical-problems / refactor write-up exists (section G).
- [ ] README, CHANGELOG, PLAN, test docs, QA report, learning log and slides match the real final state.
- [ ] `pytest` passes locally and in CI; no known leftovers remain in `QA_REPORT.md` section 2.4.

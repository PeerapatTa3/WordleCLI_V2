#!/usr/bin/env python3
"""One-time build script for the local word lists used by WordleCLI_V2.

Takes a public-domain word list (e.g. ENABLE / CSW / TWL) and filters it to
5-letter alpha words, uppercase, sorted, deduped.  Produces two output files:

    src/data/valid_words.txt  — all acceptable 5-letter words (~9-13k)
    src/data/answers.txt      — a smaller common-word subset (~1-3k)
"""

import argparse
import re
from pathlib import Path


def load_word_source(path):
    """Load raw words from a text file (one word per line, any case)."""
    words = set()
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            word = line.strip()
            if word and word.isalpha() and len(word) == 5:
                words.add(word.upper())
    return sorted(words)


def is_offensive(word):
    """Return True if the word is offensive (simple denylist)."""
    deny = {"SHITS", "FUCKS", "CUNTS", "DICKS", "PENIS", "VAGINA",
            "BITCH", "ASSES", "TITTY", "NIGGA", "PUSSY", "DAMNS"}
    return word.upper() in deny


def is_proper_noun(word):
    """Rough check — most proper nouns end with 's' are plural or
    start with a capital in normal writing.  Since our source is
    all-uppercase we rely on a small heuristic denylist instead."""
    proper = {"ALICE", "BOB", "CAROL", "DAN", "EVE", "FRANK", "JAMES",
              "JOHN", "MARY", "PAUL", "PETER", "SUSAN", "TOKYO", "PARIS",
              "LONDON", "ROME", "CAIRO", "MOSCOW", "DELHI", "CHINA",
              "JAPAN", "KOREA", "INDIA", "BRAZIL", "SWISS"}
    return word.upper() in proper


def is_plural(word):
    """Return True for words that look like regular plurals."""
    return word.endswith("S") and len(word) > 3 and word[-2] not in "'"


def filter_answers(all_words, min_commonness=1):
    """Return a subset of common, playable words unsuitable for offensive/proper/plural."""
    common = []
    for w in all_words:
        if is_offensive(w):
            continue
        if is_proper_noun(w):
            continue
        if is_plural(w):
            continue
        common.append(w)
    return common


def build_wordlists(source_path, output_dir):
    """Main build routine."""
    words = load_word_source(source_path)
    answers = filter_answers(words)

    valid_path = output_dir / "valid_words.txt"
    answers_path = output_dir / "answers.txt"

    valid_path.write_text("\n".join(words) + "\n", encoding="utf-8")
    answers_path.write_text("\n".join(answers) + "\n", encoding="utf-8")

    print(f"✓ {len(words)} valid words  → {valid_path}")
    print(f"✓ {len(answers)} answer words → {answers_path}")
    print(f"  ({len([w for w in words if w not in answers])} words only in valid list)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build Wordle word lists")
    parser.add_argument("source", help="Path to source word list (one word per line)")
    parser.add_argument(
        "-o", "--output-dir",
        default=Path(__file__).resolve().parent.parent / "src" / "data",
        help="Output directory (default: src/data/)",
    )
    args = parser.parse_args()

    src = Path(args.source)
    if not src.exists():
        print(f"❌ Source file not found: {src}")
        raise SystemExit(1)

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    build_wordlists(src, out)
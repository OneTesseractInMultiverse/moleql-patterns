# MIT License
#
# Copyright (c) 2026 Pedro Guzmán
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import annotations

from pathlib import Path

HEADER_MARKER = "MIT License"
SKIP_DIRS = {
    ".venv",
    "dist",
    "build",
    "__pycache__",
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
}
ROOT = Path(__file__).resolve().parents[1]
SEARCH_DIRS = [ROOT / "src", ROOT / "tests", ROOT / "tools"]


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def has_header(text: str) -> bool:
    return HEADER_MARKER in text[:2000]  # header should be near top


def main() -> int:
    bad: list[Path] = []
    for root in SEARCH_DIRS:
        if not root.exists():
            continue
        for path in root.rglob("*.py"):
            if should_skip(path):
                continue
            text = path.read_text(encoding="utf-8")
            if not has_header(text):
                bad.append(path.relative_to(ROOT))

    if bad:
        print("Missing MIT license header in:")
        for p in bad:
            print(f"  - {p}")
        print("\nAdd the standard header to the top of these files.")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

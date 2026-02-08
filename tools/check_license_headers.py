from __future__ import annotations

from pathlib import Path

HEADER_MARKER = "MIT License"
SKIP_DIRS = {".venv", "dist", "build", "__pycache__", ".git"}
ROOT = Path(__file__).resolve().parents[1]
PKG_DIR = ROOT / "src"


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def has_header(text: str) -> bool:
    return HEADER_MARKER in text[:2000]  # header should be near top


def main() -> int:
    bad: list[Path] = []
    for path in PKG_DIR.rglob("*.py"):
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

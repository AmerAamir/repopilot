from dataclasses import dataclass
from pathlib import Path
from collections import Counter
from .config import DEFAULT_EXCLUDES, TEXT_EXTENSIONS, IMPORTANT_FILENAMES, LANGUAGE_BY_EXTENSION

@dataclass(frozen=True)
class FileSummary:
    path: str
    extension: str
    line_count: int
    char_count: int
    preview: str

@dataclass(frozen=True)
class RepoSummary:
    root: str
    total_files_seen: int
    analyzed_files: list[FileSummary]
    skipped_files: int
    language_counts: dict[str, int]
    important_files: list[str]
    tree: str
    dependency_hints: dict[str, str]

def _skip(path: Path, root: Path, excludes: set[str]) -> bool:
    rel = path.relative_to(root)
    return any(part in excludes for part in rel.parts)

def _preview(path: Path, max_chars: int):
    text = path.read_text(encoding='utf-8', errors='replace')
    return text[:max_chars], text.count('\n') + (1 if text else 0), len(text)

def scan_repo(root_path, max_files=80, max_chars_per_file=2000, excludes=None):
    root = Path(root_path).expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f'Path is not a directory: {root}')
    excluded = set(DEFAULT_EXCLUDES)
    if excludes:
        excluded.update(excludes)
    all_files = [p for p in root.rglob('*') if p.is_file() and not _skip(p, root, excluded)]
    candidates = [p for p in all_files if p.name in IMPORTANT_FILENAMES or p.suffix in TEXT_EXTENSIONS]
    selected = sorted(candidates, key=lambda p: str(p.relative_to(root)))[:max_files]
    analyzed = []
    languages = Counter()
    important = []
    hints = {}
    for path in selected:
        rel = str(path.relative_to(root))
        text, lines, chars = _preview(path, max_chars_per_file)
        if path.suffix in LANGUAGE_BY_EXTENSION:
            languages[LANGUAGE_BY_EXTENSION[path.suffix]] += 1
        if path.name in IMPORTANT_FILENAMES:
            important.append(rel)
            hints[path.name] = text[:2500]
        analyzed.append(FileSummary(rel, path.suffix or path.name, lines, chars, text))
    tree_items = sorted(str(p.relative_to(root)) for p in all_files)[:180]
    tree = '\n'.join(tree_items)
    return RepoSummary(str(root), len(all_files), analyzed, max(0, len(all_files)-len(selected)), dict(languages), important, tree, hints)

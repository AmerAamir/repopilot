import argparse
import sys
from pathlib import Path
from .llm import LLMError, generate_docs
from .scanner import scan_repo
from .writer import write_docs

def build_parser():
    parser = argparse.ArgumentParser(prog='repopilot', description='Generate README and architecture docs from a local repository.')
    parser.add_argument('path', help='Path to the repository or project folder to analyze.')
    parser.add_argument('--out', default='repopilot-output', help='Output directory for generated Markdown files.')
    parser.add_argument('--max-files', type=int, default=80, help='Maximum files to analyze.')
    parser.add_argument('--max-chars-per-file', type=int, default=2000, help='Maximum preview characters per file.')
    parser.add_argument('--exclude', action='append', default=[], help='Additional file or folder names to exclude.')
    parser.add_argument('--no-llm', action='store_true', help='Use deterministic fallback instead of an external LLM.')
    return parser

def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        summary = scan_repo(args.path, max_files=args.max_files, max_chars_per_file=args.max_chars_per_file, excludes=args.exclude)
        docs = generate_docs(summary, force_heuristic=args.no_llm)
        written = write_docs(docs, summary, args.out)
    except (ValueError, LLMError) as exc:
        print(f'RepoPilot error: {exc}', file=sys.stderr)
        return 1
    print('RepoPilot generated documentation:')
    for path in written:
        print(f'- {Path(path)}')
    print(f"Generator: {'LLM' if docs.used_llm else 'deterministic fallback'} ({docs.model})")
    return 0

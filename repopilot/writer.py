from pathlib import Path

def write_docs(docs, summary, out_dir):
    destination = Path(out_dir).expanduser().resolve()
    destination.mkdir(parents=True, exist_ok=True)
    files = {
        'README.md': docs.readme,
        'ARCHITECTURE.md': docs.architecture,
        'REPOPILOT_REPORT.md': build_report(docs, summary),
    }
    written = []
    for name, content in files.items():
        path = destination / name
        path.write_text(content.rstrip() + '\n', encoding='utf-8')
        written.append(path)
    return written

def build_report(docs, summary):
    languages = '\n'.join(f'- {k}: {v}' for k, v in summary.language_counts.items()) or '- Unknown'
    important = '\n'.join(f'- `{p}`' for p in summary.important_files) or '- None'
    return f'''# RepoPilot Report\n\n## Generation\n\n- Used external LLM: `{docs.used_llm}`\n- Model: `{docs.model}`\n- Repository root: `{summary.root}`\n- Total files seen: `{summary.total_files_seen}`\n- Files analyzed: `{len(summary.analyzed_files)}`\n- Files skipped by limit: `{summary.skipped_files}`\n\n## Detected Languages\n\n{languages}\n\n## Important Files\n\n{important}\n\n## Tree Snapshot\n\n```text\n{summary.tree}\n```\n'''.strip()

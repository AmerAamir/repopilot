# RepoPilot

**RepoPilot** is a GitHub-ready LLM project that scans a local code repository and generates useful documentation:

- `README.md`
- `ARCHITECTURE.md`
- `REPOPILOT_REPORT.md`

It can use an OpenAI-compatible chat completions API when you provide an API key, but it also includes a deterministic fallback generator so the project works immediately without paid services.

## Why this project is useful

Many repositories have weak or outdated docs. RepoPilot helps developers quickly understand a codebase, publish cleaner GitHub repos, and bootstrap documentation before a release or portfolio submission.

## Features

- Scans source files while ignoring noisy folders like `.git`, `node_modules`, `venv`, `dist`, and build folders.
- Detects common languages and setup files.
- Builds a compact repository tree snapshot.
- Generates README and architecture documentation.
- Supports OpenAI-compatible LLM endpoints through environment variables.
- Works offline with a no-key fallback mode.
- Includes tests and a GitHub Actions workflow.

## Installation

From the project root:

```bash
python -m pip install -e .
```

## Quick Start

Generate docs for any local repo:

```bash
repopilot /path/to/your/repo --out generated-docs
```

Or run without installing:

```bash
python -m repopilot /path/to/your/repo --out generated-docs
```

## Use an LLM

Set an API key and model:

```bash
export REPOPILOT_API_KEY="your-api-key"
export REPOPILOT_MODEL="gpt-4o-mini"
```

Optional: point to any OpenAI-compatible endpoint:

```bash
export REPOPILOT_BASE_URL="https://api.openai.com/v1"
```

Then run:

```bash
repopilot . --out generated-docs
```

## Use the fallback generator

```bash
repopilot . --out generated-docs --no-llm
```

This mode is useful for demos, tests, and environments without network access.

## Example Output

RepoPilot writes:

```text
generated-docs/
├── README.md
├── ARCHITECTURE.md
└── REPOPILOT_REPORT.md
```

## Configuration

Useful options:

```bash
repopilot . \
  --out generated-docs \
  --max-files 120 \
  --max-chars-per-file 3000 \
  --exclude tmp \
  --exclude large-data
```

## Development

Run tests:

```bash
python -m unittest discover -s tests
```

## Roadmap

- Add GitHub URL cloning.
- Add issue and PR documentation generation.
- Add Mermaid diagrams for architecture output.
- Add file-level summaries cached between runs.
- Add a web UI for non-technical users.

## License

MIT

# Contributing

Thanks for helping improve RepoPilot.

## Local Setup

```bash
python -m pip install -e .
python -m unittest discover -s tests
```

## Pull Request Checklist

- Keep the CLI simple.
- Add or update tests for behavior changes.
- Do not log secrets or API keys.
- Prefer deterministic behavior in fallback mode.

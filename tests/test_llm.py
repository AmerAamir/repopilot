import tempfile
import unittest
from pathlib import Path
from repopilot.llm import generate_docs
from repopilot.scanner import scan_repo

class LLMTests(unittest.TestCase):
    def test_fallback_docs_are_generated(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'main.py').write_text("def main():\n    return 'ok'\n", encoding='utf-8')
            summary = scan_repo(root)
            docs = generate_docs(summary, force_heuristic=True)
            self.assertFalse(docs.used_llm)
            self.assertIn('#', docs.readme)
            self.assertIn('Architecture', docs.architecture)

if __name__ == '__main__':
    unittest.main()

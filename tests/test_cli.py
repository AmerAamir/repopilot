import tempfile
import unittest
from pathlib import Path
from repopilot.cli import main

class CLITests(unittest.TestCase):
    def test_cli_writes_docs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'project'
            out = Path(tmp) / 'out'
            root.mkdir()
            (root / 'main.py').write_text("print('hi')\n", encoding='utf-8')
            code = main([str(root), '--out', str(out), '--no-llm'])
            self.assertEqual(code, 0)
            self.assertTrue((out / 'README.md').exists())
            self.assertTrue((out / 'ARCHITECTURE.md').exists())
            self.assertTrue((out / 'REPOPILOT_REPORT.md').exists())

if __name__ == '__main__':
    unittest.main()

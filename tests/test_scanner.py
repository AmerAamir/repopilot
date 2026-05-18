import tempfile
import unittest
from pathlib import Path
from repopilot.scanner import scan_repo

class ScannerTests(unittest.TestCase):
    def test_scans_python_file_and_skips_git(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'app.py').write_text("print('hello')\n", encoding='utf-8')
            (root / '.git').mkdir()
            (root / '.git' / 'config').write_text('ignored', encoding='utf-8')
            summary = scan_repo(root)
            self.assertEqual(summary.total_files_seen, 1)
            self.assertEqual(len(summary.analyzed_files), 1)
            self.assertEqual(summary.analyzed_files[0].path, 'app.py')
            self.assertEqual(summary.language_counts['Python'], 1)

    def test_detects_important_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'pyproject.toml').write_text('[project]\nname="x"\n', encoding='utf-8')
            summary = scan_repo(root)
            self.assertIn('pyproject.toml', summary.important_files)

if __name__ == '__main__':
    unittest.main()

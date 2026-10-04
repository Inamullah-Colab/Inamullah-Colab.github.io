import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml
import update_citations_openalex as updater


class CitationUpdateTests(unittest.TestCase):
    def test_arxiv_doi_lookup_avoids_missing_landing_page(self):
        with patch.object(updater, "get_count_from_doi", return_value=1) as lookup:
            self.assertEqual(updater.get_count_from_arxiv("2507.12663"), 1)
            lookup.assert_called_once_with("10.48550/arXiv.2507.12663")

    def test_all_failed_requests_leave_file_and_timestamp_unchanged(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "citations.yml"
            original = "last_updated_utc: old\ntotal: 7\npapers:\n  paper:\n    source: doi\n    id: example\n    count: 7\n"
            path.write_text(original, encoding="utf-8")
            with patch.object(updater, "DATA_FILE", path), patch.object(updater, "get_count_from_doi", return_value=None):
                self.assertEqual(updater.main(), 1)
            self.assertEqual(path.read_text(encoding="utf-8"), original)

    def test_partial_failure_preserves_old_count_and_full_refresh_date(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "citations.yml"
            path.write_text("last_updated_utc: old\ntotal: 9\npapers:\n  first:\n    source: doi\n    id: a\n    count: 2\n  second:\n    source: doi\n    id: b\n    count: 7\n", encoding="utf-8")
            with patch.object(updater, "DATA_FILE", path), patch.object(updater, "get_count_from_doi", side_effect=[3, None]):
                self.assertEqual(updater.main(), 1)
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            self.assertEqual(data["total"], 10)
            self.assertEqual(data["papers"]["second"]["count"], 7)
            self.assertEqual(data["last_updated_utc"], "old")

    def test_success_including_zero_refreshes_total_and_timestamp(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "citations.yml"
            path.write_text("last_updated_utc: old\ntotal: 7\npapers:\n  paper:\n    source: doi\n    id: example\n    count: 7\n", encoding="utf-8")
            with patch.object(updater, "DATA_FILE", path), patch.object(updater, "get_count_from_doi", return_value=0):
                self.assertEqual(updater.main(), 0)
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            self.assertEqual(data["total"], 0)
            self.assertNotEqual(data["last_updated_utc"], "old")


if __name__ == "__main__":
    unittest.main()

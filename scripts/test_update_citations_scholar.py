import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import update_citations_scholar as updater


class ScholarTests(unittest.TestCase):
    def profile(self, count="25", total="25"):
        return (f'<tr class="gsc_a_tr"><td><a href="/citations?citation_for_view=owner:paper&amp;hl=en">Title</a></td>'
                f'<td><a class="gsc_a_ac gs_ibl">{count}</a></td></tr>'
                f'<table id="gsc_rsb_st"><tr><td class="gsc_rsb_std">{total}</td></tr></table>')

    def test_article_ids_and_counts(self):
        self.assertEqual(updater.parse_profile(self.profile(), "owner"), ({"paper": 25}, 25))

    def test_empty_count_means_zero(self):
        self.assertEqual(updater.parse_profile(self.profile("", "0"), "owner"), ({"paper": 0}, 0))

    def test_truncated_profile_rejected(self):
        with self.assertRaises(ValueError):
            updater.parse_profile(self.profile(total="55"), "owner")

    def test_blocked_response_does_not_change_data(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data.yml"
            markup = Path(directory) / "profile.html"
            original = "scholar_profile_id: owner\ntotal: 55\npapers: {}\n"
            path.write_text(original, encoding="utf-8")
            markup.write_text("<html>Unusual traffic</html>", encoding="utf-8")
            with patch.object(updater, "DATA_FILE", path):
                self.assertEqual(updater.main(["--html-file", str(markup)]), 1)
            self.assertEqual(path.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()

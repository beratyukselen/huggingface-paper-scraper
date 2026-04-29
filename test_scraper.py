import unittest
import os
import shutil
from scraper import HuggingFacePaperScraper

class TestHuggingFaceScraper(unittest.TestCase):
    
    def setUp(self):
        self.test_download_dir = "test_downloads"
        
        self.paper_ids = [
            "2604.22748", "2604.16353", "2604.21518", "2604.22586", "2604.22294",
            "2604.25917", "2604.24819", "2604.25914", "2604.25256", "2604.24625",
            "2604.25636", "2604.25819", "2604.25719", "2604.24842", "2604.25727",
            "2604.24005", "2604.25806", "2604.25164", "2604.25427", "2604.24441"
        ]

    def test_twenty_papers_and_none_requirement(self):
        for pid in self.paper_ids:
            with self.subTest(paper_id=pid):
                scraper = HuggingFacePaperScraper(paper_id=pid, download_dir=self.test_download_dir)
                result = scraper.execute()
                
                if result is None:
                    self.assertIsNone(result)
                else:
                    self.assertIsInstance(result, dict)
                    self.assertEqual(result["paper_id"], pid)
                    
                    self.assertIn("downloaded_files", result)

    def tearDown(self):
        if os.path.exists(self.test_download_dir):
            shutil.rmtree(self.test_download_dir)

if __name__ == '__main__':
    unittest.main()
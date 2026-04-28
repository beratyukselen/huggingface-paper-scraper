import unittest
import os
import shutil
from scraper import HuggingFacePaperScraper

class TestHuggingFaceScraper(unittest.TestCase):
    
    def setUp(self):
        self.test_paper_id = "2604.22748"
        self.test_download_dir = "test_downloads"
        self.scraper = HuggingFacePaperScraper(paper_id=self.test_paper_id, download_dir=self.test_download_dir)

    def test_initialization(self):
        self.assertEqual(self.scraper.paper_id, self.test_paper_id)
        self.assertEqual(self.scraper.download_dir, self.test_download_dir)
        self.assertTrue(os.path.exists(self.test_download_dir))

    def test_execute_returns_valid_dict(self):
        result = self.scraper.execute()
        
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["paper_id"], self.test_paper_id)
        
        self.assertIn("arxiv_link", result)
        self.assertIn("downloaded_files", result)
        
        self.assertIsNotNone(result["downloaded_files"]["pdf"])
        self.assertTrue(os.path.exists(result["downloaded_files"]["pdf"]))

    def tearDown(self):
        if os.path.exists(self.test_download_dir):
            shutil.rmtree(self.test_download_dir)

if __name__ == '__main__':
    unittest.main()
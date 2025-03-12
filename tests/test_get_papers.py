import unittest
from pubmed_fetcher.utils import fetch_paper_ids, fetch_paper_details

class TestPubMedFetcher(unittest.TestCase):
    
    def test_fetch_paper_ids(self):
        query = "cancer treatment"
        paper_ids = fetch_paper_ids(query)
        self.assertIsInstance(paper_ids, list)
    
    def test_fetch_paper_details(self):
        paper_id = "12345678"  # Example PubMed ID
        details = fetch_paper_details(paper_id)
        self.assertIsInstance(details, dict)

if __name__ == "__main__":
    unittest.main()

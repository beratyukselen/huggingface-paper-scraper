import os
import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional, Any
import re

class HuggingFacePaperScraper:
    
    def __init__(self, paper_id: str, download_dir: str = "downloads"):
        self.paper_id = paper_id
        self.base_url = f"https://huggingface.co/papers/{paper_id}"
        self.download_dir = download_dir
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

    def _get_html_dom(self) -> Optional[BeautifulSoup]:
        try:
            response = requests.get(self.base_url, headers=self.headers, timeout=10)
            if response.status_code != 200:
                return None
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException:
            return None
        
    def _download_file(self, url: str, filename: str) -> Optional[str]:
        if not url:
            return None
            
        filepath = os.path.join(self.download_dir, filename)
        try:
            response = requests.get(url, headers=self.headers, stream=True, timeout=15)
            
            content_type = response.headers.get('content-type', '').lower()
            
            if 'text/html' in content_type:
                return None

            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                return filepath
            return None
        except requests.RequestException:
            return None

    def _extract_links_from_dom(self, soup: BeautifulSoup) -> Dict[str, Optional[str]]:
        links = {
            "arxiv_url": None,
            "github_url": None,
            "project_url": None,
            "video_url": None
        }

        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            text = a_tag.get_text().lower()

            if "github.com" in href and not links["github_url"]:
                links["github_url"] = href
            
            elif "arxiv.org/abs" in href and not links["arxiv_url"]:
                links["arxiv_url"] = href
            
            elif "project" in text or "project page" in text:
                links["project_url"] = href
                
            elif any(v in href.lower() for v in [".mp4", "youtube.com/watch", "youtu.be", "vimeo.com"]):
                links["video_url"] = href

        if not links["arxiv_url"]:
             links["arxiv_url"] = f"https://arxiv.org/abs/{self.paper_id}"

        return links

    def execute(self) -> Optional[Dict[str, Any]]:
        soup = self._get_html_dom()
        
        if not soup:
            return None

        extracted_links = self._extract_links_from_dom(soup)
        
        pdf_url = f"https://arxiv.org/pdf/{self.paper_id}.pdf"
        pdf_path = self._download_file(pdf_url, f"{self.paper_id}.pdf")

        targz_url = f"https://arxiv.org/e-print/{self.paper_id}"
        targz_path = self._download_file(targz_url, f"{self.paper_id}.tar.gz")

        video_path = None
        if extracted_links["video_url"] and extracted_links["video_url"].endswith(".mp4"):
            video_name = extracted_links["video_url"].split("/")[-1]
            video_path = self._download_file(extracted_links["video_url"], video_name)

        result = {
            "paper_id": self.paper_id,
            "arxiv_link": extracted_links["arxiv_url"],
            "github_link": extracted_links["github_url"],
            "project_link": extracted_links["project_url"],
            "video_link": extracted_links["video_url"],
            "downloaded_files": {
                "pdf": pdf_path,
                "tar_gz": targz_path,
                "video": video_path
            }
        }

        return result

if __name__ == "__main__":
    test_papers = ["2604.22748", "2604.16353", "2604.21518"] 
    
    for paper_id in test_papers:
        print(f"\n--- {paper_id} için işlem başlatılıyor ---")
        scraper = HuggingFacePaperScraper(paper_id=paper_id)
        sonuc = scraper.execute()
        
        if sonuc is None:
            print(f"[{paper_id}] Bağlantı kurulamadı veya linkler yok.")
        else:
            print(f"[{paper_id}] İşlem Başarılı! İndirilen dosyalar:")
            for k, v in sonuc["downloaded_files"].items():
                print(f"  - {k}: {v}")
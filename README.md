# Hugging Face Paper Scraper

A Python automation class to scrape metadata and download research paper files (PDFs, source code archives, and videos) directly from Hugging Face paper pages.

## Features
- Scrapes arXiv, GitHub, and Project page links from the DOM.
- Automatically downloads the paper's PDF.
- Downloads the source code archive (`.tar.gz`) directly from arXiv e-prints.
- Identifies and downloads/saves video links if available.
- Gracefully handles missing files and returns `None` for unavailable data.
- OOP-based, clean structure ready to be integrated as a module.

## Requirements
- Python 3.x
- `requests`
- `beautifulsoup4`

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/beratyukselen/huggingface-paper-scraper.git
   cd huggingface-paper-scraper
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
You can easily import and use the scraper in your own projects:

```python
from scraper import HuggingFacePaperScraper

scraper = HuggingFacePaperScraper(paper_id="2604.22748")
result = scraper.execute()

print(result)
```

## Running Tests
To run the automated unit tests:
```bash
python3 -m unittest test_scraper.py
```
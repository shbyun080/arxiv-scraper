# Daily arXiv Scraper

Scrape, filter, and store daily arXiv update pages - so you don't have to.

## Setup
`pip install -r requirements.txt`

## Usage
In `main.yaml`, change `url` to desired daily update page and `filters` to your desired keyword in lower case.

`python scrape.py [--cfg <CONFIG PATH>] [--out <OUT DIR>]`

## Setting Daily

### On Windows

1. Open Task Scheduler
2. Action -> Create Basic Task
3. Choose weekly, click on day & time you want script to run
4. Start a Program -> Input path to your python exe
5. For 'add arguments' provide full path to `scrape.py` along with full path to `--cfg` and `--out`

For example, an example argument would be\
`C:arxiv-scraper\scrape.py --cfg C:arxiv-scraper\main.yaml --out C:arxiv-scraper\out`

## License
The code in this repository is released under the . A copy can be found in the LICENSE file.
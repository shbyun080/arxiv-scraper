import os
import yaml
import argparse
from datetime import datetime

import requests
from bs4 import BeautifulSoup
import re

def save_papers(papers, out='D:arXivScaper/papers.yaml'):
    with open(out, 'w') as f:
        yaml.dump(papers, f, default_flow_style=False, width=150, explicit_start=False)

def load_page(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.content
    else:
        return None
    
def load_and_parse(url):
    content = load_page(url)
    soup = BeautifulSoup(content, features='xml')

    table = soup.find('dl', attrs = {'id':'articles'})

    papers = dict()
    dts = table.find_all('dt')
    count = int(re.findall(r'\d+', table.find_next('h3').contents[0])[-1])
    for i in range(count):
        dt = dts[i]
        dd = dt.find_next_sibling('dd')
        papers[str(dd.select_one('div.list-title').contents[1].strip())] = {
            'id': 'arxiv.org/abs/{}'.format(dt.find_all('a')[1]['href'].split('/')[-1]),
            'abstract': dd.select_one('p').contents[0].strip()
        }

    return papers

def filter_papers(papers, filters=[]):
    erase_list = []
    for title in papers:
        erase = True
        title_lower = title.lower()
        for f in filters:
            if f in title_lower:
                erase = False
                break
        if erase:
            erase_list.append(title)
    
    for title in erase_list:
        del papers[title]
    
    return papers

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg', type=str, default='D:arXivScaper/main.yaml')
    parser.add_argument('--out', type=str, default='D:arXivScaper/papers')
    args = parser.parse_args()

    with open(args.cfg) as f:
        cfg = yaml.safe_load(f)

    papers = load_and_parse(cfg['url'])
    papers = filter_papers(papers, filters=cfg['filters'])
    outpath = os.path.join(args.out, 'arxiv-{}.yaml'.format(datetime.today().strftime('%Y-%m-%d')))
    save_papers(papers, out=outpath)

from apscheduler.schedulers.background import BackgroundScheduler
from services.rss import get_titles_from_rss
from services.crossref import get_doi_by_title
from services.zotero import register_doi_in_zotero
import json
import os

DOI_LOG_FILE = "data/processed_dois.json"
RSS_URL = "https://export.arxiv.org/rss/cs.AI"

def auto_import_rss():
    print("[INFO] Running scheduled RSS import...")
    titles = get_titles_from_rss(RSS_URL)
    if not titles:
        print("[WARNING] No titles found from RSS.")
        return

    if not os.path.exists(DOI_LOG_FILE):
        with open(DOI_LOG_FILE, 'w') as f:
            json.dump([], f)

    with open(DOI_LOG_FILE, 'r') as f:
        processed = set(json.load(f))

    for title in titles:
        doi = get_doi_by_title(title)
        if not doi or doi in processed:
            continue
        if register_doi_in_zotero(doi):
            processed.add(doi)

    with open(DOI_LOG_FILE, 'w') as f:
        json.dump(list(processed), f)

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(auto_import_rss, 'interval', minutes=10)
    scheduler.start()

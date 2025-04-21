from apscheduler.schedulers.background import BackgroundScheduler
from services.rss import get_titles_from_rss
from services.crossref import get_doi_by_title
from services.zotero import register_doi_in_zotero
from services.rss_targets import RSS_TARGETS
import csv, os, datetime

OUTPUT_CSV = "data/doi_log.csv"
DOI_LOG_FILE = "data/processed_dois.json"

def auto_import_all_journals():
    print("[INFO] Running scheduled journal import...")

    if not os.path.exists(DOI_LOG_FILE):
        with open(DOI_LOG_FILE, 'w') as f:
            json.dump([], f)

    with open(DOI_LOG_FILE, 'r') as f:
        processed = set(json.load(f))

    for journal, url in RSS_TARGETS.items():
        titles = get_titles_from_rss(url)
        print(f"[{journal}] Fetched {len(titles)} titles")
        for title in titles:
            doi = get_doi_by_title(title)
            if not doi or doi in processed:
                continue
            if register_doi_in_zotero(doi):
                processed.add(doi)
                save_to_csv(journal, title, doi)

    with open(DOI_LOG_FILE, 'w') as f:
        json.dump(list(processed), f)

def save_to_csv(journal, title, doi):
    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.datetime.now().isoformat(), journal, title, doi])

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(auto_import_all_journals, 'interval', minutes=10)
    scheduler.start()

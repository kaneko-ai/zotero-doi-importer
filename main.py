from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.crossref import get_doi_by_title
from services.zotero import register_doi_in_zotero
from services.rss import get_titles_from_rss
import json
import os

# FastAPI アプリの初期化
app = FastAPI()

# 登録済みDOIの記録ファイル
DOI_LOG_FILE = "data/processed_dois.json"

# --- Pydantic モデル ---
class TitleList(BaseModel):
    titles: list[str]

class RSSRequest(BaseModel):
    rss_url: str

# --- DOIから登録処理 ---
@app.post("/import/dois")
def import_dois(payload: TitleList):
    # DOI記録ファイルがなければ作成
    if not os.path.exists(DOI_LOG_FILE):
        with open(DOI_LOG_FILE, 'w') as f:
            json.dump([], f)

    # 既に登録済みのDOIを読み込み
    with open(DOI_LOG_FILE, 'r') as f:
        processed = set(json.load(f))

    result = []
    for title in payload.titles:
        doi = get_doi_by_title(title)
        if not doi:
            result.append({"title": title, "status": "DOI not found"})
            continue

        if doi in processed:
            result.append({"title": title, "doi": doi, "status": "Already processed"})
            continue

        success = register_doi_in_zotero(doi)
        if success:
            processed.add(doi)
            result.append({"title": title, "doi": doi, "status": "Registered"})
        else:
            result.append({"title": title, "doi": doi, "status": "Failed to register"})

    # 更新されたDOIリストを保存
    with open(DOI_LOG_FILE, 'w') as f:
        json.dump(list(processed), f)

    return result

# --- RSS URLからタイトル → DOI → Zotero 登録処理 ---
@app.post("/import/rss")
def import_rss(request: RSSRequest):
    titles = get_titles_from_rss(request.rss_url)
    if not titles:
        raise HTTPException(status_code=404, detail="No titles found from RSS.")
    return import_dois(TitleList(titles=titles))

from services.scheduler import start_scheduler

@app.on_event("startup")
def on_startup():
    print("[INFO] Starting background scheduler...")
    start_scheduler()

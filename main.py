from fastapi import FastAPI
from pydantic import BaseModel
from services.crossref import get_doi_by_title
from services.zotero import register_doi_in_zotero
import json, os

app = FastAPI()
DOI_LOG_FILE = "data/processed_dois.json"

class TitleList(BaseModel):
    titles: list[str]

@app.post("/import/dois")
def import_dois(payload: TitleList):
    if not os.path.exists(DOI_LOG_FILE):
        with open(DOI_LOG_FILE, 'w') as f:
            json.dump([], f)

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

    with open(DOI_LOG_FILE, 'w') as f:
        json.dump(list(processed), f)

    return result

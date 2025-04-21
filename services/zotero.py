from pyzotero import zotero
import os
from dotenv import load_dotenv

# .env を読み込み
load_dotenv()

ZOTERO_API_KEY = os.getenv("ZOTERO_API_KEY")
ZOTERO_USER_ID = os.getenv("ZOTERO_USER_ID")
ZOTERO_LIBRARY_TYPE = "user"

zot = zotero.Zotero(ZOTERO_USER_ID, ZOTERO_LIBRARY_TYPE, ZOTERO_API_KEY)

def register_doi_in_zotero(doi: str) -> bool:
    try:
        print(f"[INFO] Registering DOI in Zotero: {doi}")
        zot.create_items_from_dois([doi])
        print(f"[SUCCESS] Registered: {doi}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to register DOI: {doi}")
        print(f"[DETAIL] Exception: {e}")
        return False

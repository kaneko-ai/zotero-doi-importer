from pyzotero import zotero
import os
from dotenv import load_dotenv

# .env を読み込み
load_dotenv()

# 環境変数から API キーなどを取得
ZOTERO_API_KEY = os.getenv("ZOTERO_API_KEY")
ZOTERO_USER_ID = os.getenv("ZOTERO_USER_ID")
ZOTERO_LIBRARY_TYPE = "user"  # 個人アカウントの場合は "user"、グループの場合は "group"

# PyZotero オブジェクト生成
zot = zotero.Zotero(ZOTERO_USER_ID, ZOTERO_LIBRARY_TYPE, ZOTERO_API_KEY)

def register_doi_in_zotero(doi: str) -> bool:
    try:
        zot.create_items_from_dois([doi])
        return True
    except Exception as e:
        print(f"[ERROR] Zotero登録失敗: {doi} → {e}")
        return False

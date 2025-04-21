# Zotero DOI Importer

FastAPIベースのAPI。論文タイトルからDOIを取得し、Zoteroに自動登録します。

## 実行方法

```bash
uvicorn main:app --reload
```

## 環境変数（.env）

```
ZOTERO_API_KEY=your_api_key
ZOTERO_USER_ID=your_user_id
```

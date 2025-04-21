# Zotero DOI Importer

FastAPIベースのAPI。論文タイトルからDOIを取得し、Zoteroに自動登録します。

## 実行方法

```bash
uvicorn main:app --reload
```

## 環境変数（.env）

```
ZOTERO_API_KEY=Paper DOI 用
ZOTERO_USER_ID=3hfwGmoRQX4ZMTXbP1Hl4TG8
```

import feedparser

def get_titles_from_rss(rss_url: str) -> list[str]:
    """
    RSS URLから論文タイトル一覧を取得する
    """
    feed = feedparser.parse(rss_url)
    titles = [entry.get("title", "") for entry in feed.entries if "title" in entry]
    return titles

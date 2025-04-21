import feedparser

def get_titles_from_rss(rss_url: str) -> list[str]:
    feed = feedparser.parse(rss_url)
    titles = [entry.get("title", "") for entry in feed.entries]
    return titles

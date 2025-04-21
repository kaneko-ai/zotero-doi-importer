import requests

def get_doi_by_title(title: str) -> str | None:
    url = f"https://api.crossref.org/works?query.bibliographic={title}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    items = data.get("message", {}).get("items", [])
    if not items:
        return None
    return items[0].get("DOI")

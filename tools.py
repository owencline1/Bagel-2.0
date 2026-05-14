import requests
from duckduckgo_search import DDGS


def web_search(query: str, max_results: int = 5) -> list:
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=max_results))
    return results


def pubmed_search(query: str, max_results: int = 5) -> list:
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    search_resp = requests.get(
        f"{base_url}/esearch.fcgi",
        params={
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "sort": "date",
            "retmode": "json",
        },
        timeout=10,
    )
    ids = search_resp.json()["esearchresult"]["idlist"]

    if not ids:
        return []

    summary_resp = requests.get(
        f"{base_url}/esummary.fcgi",
        params={"db": "pubmed", "id": ",".join(ids), "retmode": "json"},
        timeout=10,
    )
    data = summary_resp.json()

    results = []
    for uid in ids:
        article = data["result"].get(uid, {})
        results.append(
            {
                "title": article.get("title", ""),
                "authors": [a["name"] for a in article.get("authors", [])[:3]],
                "pubdate": article.get("pubdate", ""),
                "journal": article.get("source", ""),
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{uid}/",
            }
        )

    return results

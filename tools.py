import xml.etree.ElementTree as ET
import requests
from duckduckgo_search import DDGS

PUBMED_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def pubmed_search(query: str, max_results: int = 8) -> list:
    search_resp = requests.get(
        f"{PUBMED_BASE}/esearch.fcgi",
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
        f"{PUBMED_BASE}/esummary.fcgi",
        params={"db": "pubmed", "id": ",".join(ids), "retmode": "json"},
        timeout=10,
    )
    data = summary_resp.json()

    fetch_resp = requests.get(
        f"{PUBMED_BASE}/efetch.fcgi",
        params={"db": "pubmed", "id": ",".join(ids), "rettype": "abstract", "retmode": "xml"},
        timeout=15,
    )

    abstracts = {}
    try:
        root = ET.fromstring(fetch_resp.text)
        for article in root.findall(".//PubmedArticle"):
            pmid_el = article.find(".//PMID")
            abstract_el = article.find(".//AbstractText")
            if pmid_el is not None and abstract_el is not None:
                abstracts[pmid_el.text] = abstract_el.text or ""
    except ET.ParseError:
        pass

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
                "abstract": abstracts.get(uid, "No abstract available."),
            }
        )

    return results


def web_search(query: str, max_results: int = 5) -> list:
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=max_results))
    return results

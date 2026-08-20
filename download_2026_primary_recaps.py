#!/usr/bin/env python3
"""Download county primary recap sheet PDFs from elect.ky.gov into 2026/primary."""
import os
import time
import requests
from bs4 import BeautifulSoup

URL = "https://elect.ky.gov/results/2020-2029/Pages/2026Primary-Recap-Sheets.aspx"
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "2026", "primary")
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    )
}


def get_pdf_links():
    resp = requests.get(URL, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.lower().endswith(".pdf"):
            if href.startswith("http"):
                links.append(href)
            else:
                links.append(requests.compat.urljoin(URL, href))
    return sorted(set(links))


def download(links):
    os.makedirs(OUT_DIR, exist_ok=True)
    for link in links:
        filename = os.path.basename(link)
        dest = os.path.join(OUT_DIR, filename)
        if os.path.exists(dest):
            print(f"skip (exists): {filename}")
            continue
        print(f"downloading: {filename}")
        r = requests.get(link, headers=HEADERS, timeout=30)
        r.raise_for_status()
        with open(dest, "wb") as f:
            f.write(r.content)
        time.sleep(0.5)


if __name__ == "__main__":
    pdf_links = get_pdf_links()
    print(f"found {len(pdf_links)} PDFs")
    download(pdf_links)

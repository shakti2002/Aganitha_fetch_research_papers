import requests
import pandas as pd
import argparse
import re
from typing import List, Dict, Optional
from dotenv import load_dotenv
import os
# PubMed API Base URL
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(env_path)
PUBMED_API_URL = os.getenv("PUBMED_API_URL")
PUBMED_SUMMARY_URL = os.getenv("PUBMED_SUMMARY_URL")
PUBMED_FETCH_URL =os.getenv("PUBMED_FETCH_URL")
# List of keywords that indicate academic institutions
ACADEMIC_KEYWORDS = ["university", "college", "institute", "school", "research center", "hospital"]

def fetch_paper_ids(query: str, debug: bool = False) -> List[str]:
    """Fetch paper IDs from PubMed API based on query."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": 50,  # Fetch up to 50 results
        "retmode": "json"
    }
    response = requests.get(PUBMED_API_URL, params=params)
    if debug:
        print(f"PubMed API Response: {response.json()}")
    
    response.raise_for_status()
    data = response.json()
    return data.get("esearchresult", {}).get("idlist", [])

def fetch_paper_details(paper_ids: List[str], debug: bool = False) -> List[Dict]:
    """Fetch paper details from PubMed API using paper IDs."""
    if not paper_ids:
        return []

    params = {
        "db": "pubmed",
        "id": ",".join(paper_ids),
        "retmode": "xml"
    }
    response = requests.get(PUBMED_FETCH_URL, params=params)
    response.raise_for_status()

    if debug:
        print("Fetched Paper Details:", response.text[:500])  # Print first 500 chars for debug
    
    return parse_paper_data(response.text)

def parse_paper_data(xml_data: str) -> List[Dict]:
    """Parse XML response to extract relevant paper details."""
    from xml.etree import ElementTree as ET

    root = ET.fromstring(xml_data)
    papers = []
    
    for article in root.findall(".//PubmedArticle"):
        paper_id = article.find(".//PMID").text
        title = article.find(".//ArticleTitle").text
        pub_date = article.find(".//PubDate/Year")
        pub_date = pub_date.text if pub_date is not None else "Unknown"
        
        authors = []
        company_affiliations = []
        corresponding_email = None

        for author in article.findall(".//Author"):
            name = author.find("LastName")
            if name is not None:
                full_name = name.text
                affiliation = author.find("AffiliationInfo/Affiliation")

                if affiliation is not None:
                    affiliation_text = affiliation.text.lower()
                    if any(keyword in affiliation_text for keyword in ACADEMIC_KEYWORDS):
                        continue  # Skip academic authors
                    
                    authors.append(full_name)
                    company_affiliations.append(affiliation.text)
        
        email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", xml_data)
        if email_match:
            corresponding_email = email_match.group(0)

        if authors:
            papers.append({
                "PubmedID": paper_id,
                "Title": title,
                "Publication Date": pub_date,
                "Non-academic Author(s)": ", ".join(authors),
                "Company Affiliation(s)": ", ".join(company_affiliations),
                "Corresponding Author Email": corresponding_email
            })

    return papers

def save_to_csv(papers: List[Dict], filename: str):
    """Save results to CSV file."""
    df = pd.DataFrame(papers)
    df.to_csv(filename, index=False)
    print(f"Results saved to {filename}")

def main():
    """Main function for command-line execution."""
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with non-academic authors.")
    parser.add_argument("query", type=str, help="Search query for PubMed API")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("-f", "--file", type=str, help="Filename to save output (CSV)")

    args = parser.parse_args()

    paper_ids = fetch_paper_ids(args.query, args.debug)
    if not paper_ids:
        print("No papers found.")
        return

    papers = fetch_paper_details(paper_ids, args.debug)
    
    if args.file:
        save_to_csv(papers, args.file)
    else:
        print(pd.DataFrame(papers))

if __name__ == "__main__":
    main()




import argparse
import requests
import pandas as pd
from pubmed_fetcher.utils import fetch_paper_ids, fetch_paper_details, save_to_csv

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="Search query for PubMed.")
    parser.add_argument("-f", "--file", type=str, help="Filename to save the results.", default="data/results.csv")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")
    
    args = parser.parse_args()

    if args.debug:
        print(f"Searching PubMed for: {args.query}")

    paper_ids = fetch_paper_ids(args.query)

    if args.debug:
        print(f"Found Paper IDs: {paper_ids}")

    papers = []
    for paper_id in paper_ids:
        details = fetch_paper_details(paper_id)
        if details:
            papers.append(details)
    
    save_to_csv(papers, args.file)

if __name__ == "__main__":
    main()

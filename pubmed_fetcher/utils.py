import requests
import pandas as pd
import xml.etree.ElementTree as ET

PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

def fetch_paper_ids(query):
    """Fetches paper IDs from PubMed based on a user query."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 10  # Adjust as needed
    }
    response = requests.get(PUBMED_API_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data.get("esearchresult", {}).get("idlist", [])
    else:
        print("Error fetching paper IDs:", response.status_code)
        return []

def fetch_paper_details(paper_id):
    """Fetches paper details using PubMed's efetch API."""
    params = {
        "db": "pubmed",
        "id": paper_id,
        "retmode": "xml"
    }
    response = requests.get(PUBMED_FETCH_URL, params=params)
    
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        article = root.find(".//PubmedArticle")
        
        if article is not None:
            pubmed_id = paper_id
            title = article.find(".//ArticleTitle").text if article.find(".//ArticleTitle") is not None else "N/A"
            pub_date = article.find(".//PubDate/Year").text if article.find(".//PubDate/Year") is not None else "N/A"
            
            # Extract authors and affiliations
            authors = []
            company_affiliations = []
            corresponding_email = "N/A"
            
            for author in article.findall(".//Author"):
                name = " ".join(filter(None, [
                    author.find("ForeName").text if author.find("ForeName") is not None else "",
                    author.find("LastName").text if author.find("LastName") is not None else ""
                ]))
                
                affiliation = author.find("AffiliationInfo/Affiliation")
                if affiliation is not None:
                    affiliation_text = affiliation.text.lower()
                    if "pharma" in affiliation_text or "biotech" in affiliation_text:
                        company_affiliations.append(affiliation.text)
                    else:
                        authors.append(name)
                
                # Extract corresponding author email if present
                email = author.find(".//ElectronicAddress")
                if email is not None:
                    corresponding_email = email.text
            
            return {
                "PubmedID": pubmed_id,
                "Title": title,
                "Publication Date": pub_date,
                "Non-academic Author(s)": "; ".join(authors),
                "Company Affiliation(s)": "; ".join(company_affiliations),
                "Corresponding Author Email": corresponding_email
            }
    
    return None

def save_to_csv(papers, filename="data/results.csv"):
    """Saves paper details to a CSV file."""
    df = pd.DataFrame(papers)
    df.to_csv(filename, index=False)
    print(f"Results saved to {filename}")

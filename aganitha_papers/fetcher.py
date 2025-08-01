from typing import List, Dict
import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

PHARMA_KEYWORDS = [
    "pharma", "biotech", "therapeutics", "laboratories", "inc", "llc", "gmbh",
    "ltd", "genentech", "pfizer", "novartis", "astrazeneca", "gilead", "sanofi",
    "roche", "abbvie", "company", "corporation", "corp", "private limited"
]

ACADEMIC_KEYWORDS = ["university", "college", "institute", "school", "hospital", "faculty", "department"]


def search_pubmed(query: str) -> List[str]:
    """Search PubMed and return list of paper IDs"""
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": 100,
        "retmode": "json"
    }
    
    try:
        response = requests.get(BASE_URL + "esearch.fcgi", params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if "esearchresult" not in data or "idlist" not in data["esearchresult"]:
            return []
            
        return data["esearchresult"]["idlist"]
    except requests.RequestException as e:
        print(f"Error searching PubMed: {e}")
        return []
    except KeyError as e:
        print(f"Unexpected response format: {e}")
        return []


def is_pharma_affiliation(affiliations: List[str]) -> bool:
    """Check if any affiliation appears to be pharmaceutical/industry"""
    for aff in affiliations:
        aff_lower = aff.lower()
        if any(pharma in aff_lower for pharma in PHARMA_KEYWORDS) and not any(acad in aff_lower for acad in ACADEMIC_KEYWORDS):
            return True
    return False


def fetch_pubmed_details(paper_ids: List[str]) -> List[Dict]:
    """Fetch detailed information for given PubMed IDs"""
    if not paper_ids:
        return []
    
    # Process in batches to avoid overwhelming the API
    batch_size = 50
    all_articles = []
    
    for i in range(0, len(paper_ids), batch_size):
        batch = paper_ids[i:i + batch_size]
        ids = ",".join(batch)
        
        params = {
            "db": "pubmed",
            "id": ids,
            "retmode": "xml",
        }
        
        try:
            response = requests.get(BASE_URL + "efetch.fcgi", params=params, timeout=30)
            response.raise_for_status()
            
            # Parse XML with proper error handling
            soup = BeautifulSoup(response.content, "xml")  # Using 'xml' parser instead
            
            for article in soup.find_all("PubmedArticle"):
                # PubMed ID
                pmid_tag = article.find("PMID")
                pubmed_id = pmid_tag.text if pmid_tag else "N/A"

                # Title
                title_tag = article.find("ArticleTitle")
                title = title_tag.text if title_tag else "N/A"

                # Journal
                journal_tag = article.find("Title")
                journal = journal_tag.text if journal_tag else "N/A"

                # Publication Date
                pub_date_tag = article.find("PubDate")
                pub_year = pub_date_tag.find("Year").text if pub_date_tag and pub_date_tag.find("Year") else "N/A"

                # Authors and Affiliations
                authors = []
                affiliations = []
                for author in article.find_all("Author"):
                    last = author.find("LastName")
                    fore = author.find("ForeName")
                    name = f"{fore.text if fore else ''} {last.text if last else ''}".strip()
                    if name:
                        authors.append(name)

                    for aff_tag in author.find_all("Affiliation"):
                        affiliations.append(aff_tag.text)

                paper = {
                    "pubmed_id": pubmed_id,
                    "title": title,
                    "journal": journal,
                    "year": pub_year,
                    "authors": "; ".join(authors),
                    "affiliations": "; ".join(affiliations),
                    "has_pharma_author": is_pharma_affiliation(affiliations)
                }

                all_articles.append(paper)
                
            # Be nice to NCBI servers
            if i + batch_size < len(paper_ids):
                time.sleep(0.5)
                
        except requests.RequestException as e:
            print(f"Error fetching details for batch {i//batch_size + 1}: {e}")
            continue
        except Exception as e:
            print(f"Error parsing XML for batch {i//batch_size + 1}: {e}")
            continue

    return all_articles
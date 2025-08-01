# 🧪 PubMed Pharma Paper Scraper

A Python-based CLI tool to search PubMed for scientific publications, fetch detailed metadata, and detect pharmaceutical or industrial authorship using affiliation analysis.

## 🔍 What It Does

- Searches PubMed for a given query 
- Fetches metadata such as:
  - PubMed ID
  - Title
  - Authors
  - Journal
  - Year of publication
  - Affiliations
  - Indicator if any author has a pharma/industry affiliation
- Detects pharma authors based on keywords in affiliations
- Saves results as a CSV file or prints them as JSON

## 🛠️ Project Structure

aganitha_papers/
├── fetcher.py   # Handles PubMed API requests, XML parsing, and pharma detection
├── utils.py     # Utility for saving data to CSV
├── cli.py       # Typer-based CLI for interacting with the tool



## 🚀 Usage

You can run the CLI tool with the following command:

python -m aganitha_papers.cli get "your search query" -f output.csv -d


## 🧠 How Pharma Detection Works

The script checks all author affiliations against a set of pharma/industry keywords like:

"pharma", "biotech", "inc", "gmbh", "llc", "pfizer", "novartis", "roche", etc.

If such keywords appear in the affiliation without academic keywords like:

"university", "college", "institute", "faculty", etc.

...the paper is flagged as having a pharma author.



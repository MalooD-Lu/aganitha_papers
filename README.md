# 🧪 PubMed Pharma Paper Scraper

A Python-based CLI tool to search PubMed for scientific publications, fetch detailed metadata, and detect pharmaceutical or industrial authorship using affiliation analysis.

---

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

---

## 🛠️  Code Organization

```
aganitha_papers/
├── __init__.py        # (Optional) package initializer
├── fetcher.py         # Contains logic for PubMed API requests, parsing responses, and pharma affiliation detection
├── utils.py           # Contains utility functions (e.g., CSV export)
├── cli.py             # Typer-based CLI that connects everything and handles user interaction
```

- **`fetcher.py`**: Handles querying PubMed and parsing metadata from XML. Also includes the logic for checking pharma/academic affiliations.
- **`utils.py`**: Contains a helper function to save the extracted data into a CSV file.
- **`cli.py`**: Defines a CLI using the `typer` package. Accepts search queries, prints or saves results, and includes debug output.

---

## ⚙️ Installation & Usage

### 1. Clone the repository:

```bash
git clone https://github.com/MalooD-Lu/aganitha_papers.git
cd aganitha_papers
```

### 2. Install dependencies:

It is recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the CLI tool:

```bash
python -m aganitha_papers.cli get "your search query" -f output.csv -d
```

### Example:

```bash
python -m aganitha_papers.cli get "breast cancer therapy" -f results.csv -d
```

- `--file` or `-f`: Optional output CSV file.
- `--debug` or `-d`: Optional debug flag to show logs.

---

## 🧠 How Pharma Detection Works

The script checks all author affiliations against a set of pharma/industry keywords like:

"pharma", "biotech", "inc", "gmbh", "llc", "pfizer", "novartis", "roche", etc.

If such keywords appear in the affiliation without academic keywords like:

"university", "college", "institute", "faculty", etc.

...the paper is flagged as having a pharma author.

---

## 🧰 Tools & Libraries Used

- **[Typer](https://typer.tiangolo.com/)**: For building the command-line interface
- **[Requests](https://docs.python-requests.org/)**: For sending HTTP requests to the PubMed Entrez API
- **[BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)**: For parsing XML responses
- **[Pandas](https://pandas.pydata.org/)**: For handling tabular data and exporting to CSV
- **[PubMed Entrez API](https://www.ncbi.nlm.nih.gov/books/NBK25501/)**: Source of biomedical literature

---



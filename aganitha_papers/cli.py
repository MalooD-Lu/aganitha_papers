import typer
from aganitha_papers.fetcher import search_pubmed, fetch_pubmed_details 
from aganitha_papers.utils import save_to_csv
import json

app = typer.Typer()

@app.command() 
def get(
    query: str = typer.Argument(..., help="Query to search PubMed."),
    file: str = typer.Option(None, "-f", "--file", help="Filename to save CSV."),
    debug: bool = typer.Option(False, "-d", "--debug", help="Enable debug output.")
):
    """Search PubMed for papers and save results to CSV or print as JSON."""
    if debug:
        typer.echo(f"Searching PubMed for: {query}") 
        
    ids = search_pubmed(query)
    
    if not ids:
        typer.echo("No papers found for the given query.")
        return
        
    if debug:
        typer.echo(f"Found {len(ids)} papers.")
        
    data = fetch_pubmed_details(ids)
    
    if not data:
        typer.echo("No paper details could be retrieved.")
        return
    
    if file:
        save_to_csv(data, file)
        typer.echo(f"Saved {len(data)} entries to {file}")
    else:
        typer.echo(json.dumps(data, indent=2))

if __name__ == "__main__":
    app()

# Usage examples:
# python -m get_papers.cli get "cancer immunotherapy" -f cancer_results.csv -d
# poetry run get-papers-list get "cancer immunotherapy" -f cancer_results.csv -d
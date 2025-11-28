import os
import subprocess
import typer
from rich.console import Console
from rich.markdown import Markdown
from openai import OpenAI
from dotenv import load_dotenv

app = typer.Typer()  # <--- This creates the application
console = Console()
load_dotenv()

# ... (keep your get_git_diff and analyze_with_ai functions the same) ...

# THIS IS THE FIX: Explicitly naming the command 'audit'
@app.command() 
def audit(branch: str = typer.Option(None, help="The branch to compare against")):
    """
    Run the AI audit.
    """
    console.print(f"[bold blue]🚀 Airlock: Starting Audit...[/bold blue]")
    # ... (Your logic here) ...
    # (If you need the full function body again, let me know)

if __name__ == "__main__":
    app()

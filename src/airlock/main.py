import os
import subprocess
import typer
from rich.console import Console
from rich.markdown import Markdown
from openai import OpenAI
from dotenv import load_dotenv

# Initialize the app
app = typer.Typer()
console = Console()

# Load environment variables
load_dotenv()

def get_git_diff(branch: str = None):
    """Reads the changes. If branch is provided, compares against it."""
    try:
        if branch:
            # CI MODE: Compare against a specific branch (e.g. origin/main)
            command = ["git", "diff", branch]
        else:
            # LOCAL MODE: Compare staged files
            command = ["git", "diff", "--staged"]
            
        result = subprocess.run(
            command, 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError:
        console.print("[bold red]Error:[/bold red] Git command failed.")
        return None

def analyze_with_ai(diff_text):
    """Sends the diff to the AI for analysis."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        console.print("[bold red]Error:[/bold red] OPENAI_API_KEY not found.")
        raise typer.Exit()

    client = OpenAI(api_key=api_key)

    system_prompt = """
    You are a Senior Code Reviewer. Analyze the provided git diff.
    1. Summarize what changed in 1-2 sentences.
    2. Explain the "Why" behind the change if possible.
    3. ALERT: If you see hardcoded secrets, temporary debug code, or security risks.
    Format your response in simple Markdown.
    """

    user_prompt = f"Here is the git diff:\n\n{diff_text}"

    with console.status("[bold green]Consulting the AI agent...[/bold green]"):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
    
    return response.choices[0].message.content

@app.command()
def audit(branch: str = typer.Option(None, help="The branch to compare against")):
    """Main command to run the audit."""
    console.print(f"[bold blue]🚀 Airlock: Starting Audit (Target: {branch if branch else 'Staged'})...[/bold blue]")
    
    diff = get_git_diff(branch)
    
    if not diff:
        console.print("[yellow]No changes found.[/yellow]")
        return
        
    if len(diff) > 10000:
        console.print("[yellow]Warning: Large diff detected. Truncating...[/yellow]")
        diff = diff[:10000]

    try:
        summary = analyze_with_ai(diff)
        console.print("\n[bold]---------------- REPORT ----------------[/bold]\n")
        console.print(Markdown(summary))
        console.print("\n[bold]----------------------------------------[/bold]")
    except Exception as e:
        console.print(f"[bold red]An error occurred:[/bold red] {e}")

if __name__ == "__main__":
    app()
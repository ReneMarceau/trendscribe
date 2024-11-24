import os
import logging
import json
from dotenv import load_dotenv
from rich.console import Console
from rich.prompt import Confirm
from rich.panel import Panel
from rich.markdown import Markdown
from database import DatabaseHandler
from rss_handler import RSSHandler
from api_client import APIClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

console = Console()

def setup_environment():
    """Load environment variables and initialize clients."""
    load_dotenv()
    
    required_vars = [
        'PERPLEXITY_API_KEY',
        'OPENAI_API_KEY'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    return {
        'perplexity_api_key': os.getenv('PERPLEXITY_API_KEY'),
        'openai_api_key': os.getenv('OPENAI_API_KEY')
    }

def display_analysis(analysis):
    """Display the Perplexity API analysis result"""
    console.print("\n[bold cyan]═══ Perplexity Analysis ═══[/bold cyan]")
    
    if not analysis:
        console.print("[red]No analysis available[/red]")
        return

    # Display key insights
    if analysis.get('key_insights'):
        console.print("\n[bold blue]Key Insights:[/bold blue]")
        for insight in analysis['key_insights']:
            console.print(f"• {insight}")

    # Display technical details
    if analysis.get('technical_details'):
        console.print("\n[bold blue]Technical Details:[/bold blue]")
        for detail in analysis['technical_details']:
            console.print(f"• {detail}")

    # Display practical applications
    if analysis.get('practical_applications'):
        console.print("\n[bold blue]Practical Applications:[/bold blue]")
        for app in analysis['practical_applications']:
            console.print(f"• {app}")

    # Display considerations
    if analysis.get('considerations'):
        console.print("\n[bold blue]Important Considerations:[/bold blue]")
        for consideration in analysis['considerations']:
            console.print(f"• {consideration}")

def display_linkedin_post(post_data):
    """Display the generated LinkedIn post"""
    if not post_data or 'post' not in post_data:
        console.print("[red]No post content available[/red]")
        return

    # Create a panel with the post content
    post_panel = Panel(
        post_data['post'],
        title="[bold green]LinkedIn Post[/bold green]",
        subtitle="[dim](Copy the content below)[/dim]",
        border_style="green",
        padding=(1, 2)
    )
    
    console.print("\n")  # Add some spacing
    console.print(post_panel)
    console.print("\n")  # Add some spacing

def main():
    try:
        # Initialize components
        env_vars = setup_environment()
        db_handler = DatabaseHandler()
        rss_handler = RSSHandler("https://techcrunch.com/feed/")
        api_client = APIClient(
            perplexity_api_key=env_vars['perplexity_api_key'],
            openai_api_key=env_vars['openai_api_key']
        )

        # Fetch posts
        posts = rss_handler.fetch_posts()
        if not posts:
            console.print("[yellow]No new posts found in the feed.[/yellow]")
            return

        # Process each post
        for post in posts:
            if db_handler.is_post_processed(post.link):
                continue

            # Display the post
            rss_handler.display_post(post)

            # Ask for user confirmation
            if not Confirm.ask("Would you like to process this post?"):
                continue

            # Analyze article and generate LinkedIn post
            console.print("\n[bold]Processing article...[/bold]")
            analysis = api_client.analyze_article(post.link)
            
            # Display the analysis
            display_analysis(analysis)

            if analysis:
                linkedin_post = api_client.generate_linkedin_post({
                    'title': post.title,
                    'summary': analysis.get('summary'),
                    'sentiment': analysis.get('sentiment')
                })

                # Display the LinkedIn post
                display_linkedin_post(linkedin_post)

                if linkedin_post:
                    # Mark post as processed
                    db_handler.mark_post_processed(post.link, post.title)
                    console.print("\n[green]Post processed successfully![/green]")
            
            if not Confirm.ask("\nContinue to next post?"):
                break

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        console.print(f"[red]Error: {str(e)}[/red]")

if __name__ == "__main__":
    console.print("\n[bold blue]═══ TrendScribe - TechCrunch RSS Processor ═══[/bold blue]")
    main()

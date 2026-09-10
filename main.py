from ddgs import DDGS
from rich import print
from rich.console import Group, Console
from rich.text import Text
from rich.live import Live
from rich.spinner import Spinner
import sys
import shutil
import questionary
import readchar
import requests
from bs4 import BeautifulSoup
import os
from google import genai
from faker import Faker

fake = Faker()
width = shutil.get_terminal_size().columns
client = genai.Client()
console = Console()
KEYBINDS = Text("[Q]uit     [S]ummarize page", style="bold black on white")

class StatusBar:
    def __init__(self, console):
        self.spinner = None
        self.console = console
        self.live = Live(self._render(), refresh_per_second=8, screen=False, transient=False, console=self.console)

    def _render(self):
        if self.spinner:
            return Group(self.spinner, KEYBINDS)
        return Group(KEYBINDS)

    def start(self):
        self.live.start()

    def stop(self):
        self.live.stop()

    def set(self, text, spinner_style="arc"):
        self.spinner = Spinner(spinner_style, text)
        self.live.update(self._render())

    def clear(self):
        self.spinner = None
        self.live.update(self._render())

status_bar = StatusBar(console)


def main():
    status_bar.start()

    if len(sys.argv) != 2:
        console.print("[bold red]No query provided[/bold red]")
        status_bar.stop()
        return

    query = sys.argv[1]
    results = search(query)

    for res in results:
        console.print(f'[bold blue]{res['title']}[/bold blue]')
        console.print(f'[italic]{res['href']}[italic]')
        console.print('')
        console.print(res['body'])
        console.print('')
        console.print('-' * width)
        console.print('')

    while True:
        key = readchar.readkey()
        if key == 's':
            urls = map(lambda res: res['href'], results)
            url = questionary.select(
                "Select Url: ",
                list(urls)
            ).ask()
            summarizeUrl(url)
        elif key == 'q':
            break

    status_bar.stop()

def summarizeUrl(url):
    headers = {
        'User-Agent': fake.firefox()
    }
    status_bar.set("[bold blue]Fetching URL...")
    res = requests.get(url, headers=headers)
    status_bar.clear()
    if res.status_code != 200:
        console.print("[red bold]Error fetching the url[/red bold]")
        console.print(f'[red bold]Status code:[/red bold] {res.status_code}')
        return
    console.print("[blue bold]Fetched Url")
    soup = BeautifulSoup(res.text, 'html.parser')
    for tag in soup(['script', 'style', 'noscript', 'svg', 'nav', 'footer']):
        tag.decompose()

    content = soup.get_text(separator='\n', strip=True)
    status_bar.set('[bold blue]Summarizing...')
    interaction = client.interactions.create(
        model = "gemini-3.8-flash",
        input = f'''
            You are an expert at summarizing webpages to tell users all the key information a page contains by analysing the html of the page. 
            Always output in a form the can be processed by the rich python library. This means surronding text in appropriate colors or decorations.
            You must always put closing tags for any decorated text. For example, the response must look like [options]Text here[/options], where options is replaced with colors like red or blue or font decorations like bold or italic.
            You may add mutiple options to this rich text.
            Analyse this html and present the results in appropriately styled plain text: {content}
            '''
    )
    status_bar.clear()
    console.print(interaction.output_text)


def search(query):
    status_bar.set("[bold blue]Searching")
    results = DDGS().text(query, max_results=5)
    status_bar.clear()
    return results

if __name__ == "__main__":
    main()



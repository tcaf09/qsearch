from ddgs import DDGS
from rich import print
import sys
import shutil
import questionary
import readchar
import requests
from bs4 import BeautifulSoup

width = shutil.get_terminal_size().columns

def main():
    if len(sys.argv) != 2:
        print("[bold red]No query provided[/bold red]")
        return
    else:
        query = sys.argv[1]

    results = search(query)

    for res in results:
        print(f'[bold blue]{res['title']}[/bold blue]')
        print(f'[italic]{res['href']}[italic]')
        print('')
        print(res['body'])
        print('')
        print('-' * width)
        print('')

    while True:
        key = readchar.readkey()
        if key == 'o':
            urls = map(lambda res: res['href'], results)
            openUrl(list(urls))

def openUrl(urls):
    url = questionary.select(
        "Select Url",
        urls
    ).ask()
    res = requests.get(url)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        print(soup.prettify())
    else:
        print('[bold red] Failed to fetch page[/bold red]')
        print(f'Status code: {res.status_code}')

def search(query):
    results = DDGS().text(query, max_results=5)
    return results

if __name__ == "__main__":
    main()



import os
import json
import requests
from bs4 import BeautifulSoup
from graphviz import Digraph

def get_text_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch content from {url}")
        return None

def find_word_occurrences(text, keywords):
    occurrences = {keyword: text.lower().count(keyword.lower()) for keyword in keywords}
    return occurrences

def create_flowchart(links_data, target_word):
    dot = Digraph(comment='Word Occurrences Flowchart', format='png', engine='dot', graph_attr={'rankdir': 'LR'})

    for link, occurrences in links_data.items():
        node_label = f"{link}\nOccurrences: {', '.join(f'{key}: {count}' for key, count in occurrences.items())}"
        dot.node(link, node_label)

    for link, occurrences in links_data.items():
        edge_label = f"Occurrences: {', '.join(f'{key}: {count}' for key, count in occurrences.items())}"
        dot.edge(link, edge_label)

    dot.render('word_occurrences_flowchart', format='png', cleanup=True)

if __name__ == "__main__":
    with open('links.json', 'r') as file:
        data = json.load(file)

    links = data.get('links', [])
    keywords = data.get('keywords', [])
    target_word = data.get('target_word', '')

    links_data = {}

    for link in links:
        text = get_text_from_url(link)
        if text:
            occurrences = find_word_occurrences(text, keywords)
            links_data[link] = occurrences

    print("Word Occurrences:")
    for link, occurrences in links_data.items():
        print(f"{link}: {occurrences} occurrences")

    create_flowchart(links_data, target_word)
    print("Flowchart created: word_occurrences_flowchart.png")

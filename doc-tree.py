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

def create_flowchart(sections_data, target_word):
    dot = Digraph(comment='Word Occurrences Flowchart', format='png', engine='dot', graph_attr={'rankdir': 'LR'})

    # Predefined set of colors
    colors = ['lightblue', 'lightgreen', 'lightpink', 'lightyellow', 'lightcoral', 'lightsalmon', 'lightcyan']

    for i, section in enumerate(sections_data):
        section_title = section.get('title', 'Untitled Section')
        section_subgraph = Digraph(comment=f'{section_title} Subgraph', graph_attr={'rankdir': 'LR'})
        section_subgraph.node(section_title, label=f"{section_title}\n(Section)", shape='box', style='filled', fillcolor=colors[i % len(colors)])

        for link_info in section.get('links', []):
            link = link_info.get('link')
            occurrences = link_info.get('occurrences', {})

            text = get_text_from_url(link)
            if text:
                node_label = f"{link}\nOccurrences: {', '.join(f'{key}: {count}' for key, count in occurrences.items())}"
                section_subgraph.node(link, node_label, fillcolor=colors[i % len(colors)], style='filled')
                section_subgraph.edge(section_title, link)

        dot.subgraph(section_subgraph)

    dot.render('word_occurrences_flowchart', format='png', cleanup=True)

if __name__ == "__main__":
    with open('links.json', 'r') as file:
        data = json.load(file)

    sections = data.get('sections', [])
    keywords = data.get('keywords', [])
    target_word = data.get('target_word', '')

    sections_data = []

    for section in sections:
        section_title = section.get('title', 'Untitled Section')
        section_links = section.get('links', [])

        section_data = {'title': section_title, 'links': []}

        for link_info in section_links:
            link = link_info.get('link')
            occurrences = find_word_occurrences(get_text_from_url(link), keywords)
            section_data['links'].append({'link': link, 'occurrences': occurrences})

        sections_data.append(section_data)

    print("Word Occurrences:")
    for section_data in sections_data:
        section_title = section_data['title']
        section_links = section_data['links']
        print(f"\nSection: {section_title}")
        for link_occurrences in section_links:
            link, occurrences = link_occurrences['link'], link_occurrences['occurrences']
            print(f"{link}: {occurrences} occurrences")

    create_flowchart(sections_data, target_word)
    print("Flowchart created: word_occurrences_flowchart.png")

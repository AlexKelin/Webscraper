import contextlib
from bs4 import BeautifulSoup
import requests
import re
import sqlite3


def get_model():
    return input("What video card model you want to search for? ")


def get_clean_page(search_term):
    url = f"https://www.newegg.ca/p/pl?d={search_term}&N=4131"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")
    page_text = doc.find(class_='list-tool-pagination-text').strong
    pages = int(str(page_text).split('/')[-2].split('>')[-1][:-1])
    return pages, doc


def parse_page(pages, doc, search_term):
    items_found = {}
    for page in range(1, pages + 1):
        url = f"https://www.newegg.ca/p/pl?d={search_term}&N=4131&page={page}"
        page = requests.get(url).text
        div = doc.find(class_='item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell')
        items = div.find_all(text=re.compile(search_term))
        for item in items:
            parent = item.parent
            if parent.name != "a":
                continue
            link = parent['href']
            next_parent = item.find_parent(class_="item-container")
            with contextlib.suppress(Exception):
                price = next_parent.find(class_="price-current").strong.string
                items_found[item] = {"price": int(price.replace(",", "")), "link": link}
    print(items_found)
    sorted_items = sorted(items_found.items(), key=lambda x: x[1]['price'])
    for item in sorted_items:
        print(item[0])
        print(f"${item[1]['price']}")
        print(item[1]['link'])
        print('___________________________________')
    return sorted_items


def store_data(sorted_items):
    conn = sqlite3.connect('info.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS info
                    (name text, price integer, link text)''')
    for item in sorted_items:
        c.execute("INSERT INTO newegg VALUES (?, ?, ?)", (item[0], item[1]['price'], item[1]['link']))
    conn.commit()
    conn.close()


def main():
    choice = get_model()
    material, document = get_clean_page(choice)
    result = parse_page(material, document, choice)
    store_data(result)


if __name__ == '__main__':
    main()







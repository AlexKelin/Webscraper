# Getting info from multiple websites

from bs4 import BeautifulSoup
import requests
import re
import sqlite3

search_term = input("what product you want to search for?")

url = f"https://www.newegg.ca/p/pl?d={search_term}&N=4131"  # &N = 4131 is a
# filter of only in stock
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")
items_found = {}  # WE put the results here
# There are multiple pages on search result, we need to know how much pages
# total there is and get the number = "list-tool-pagination-text" section in HTML
# page_text = doc.find(class_='list-tool-pagination-text')

# Enter the moddel type we want :3080
# And we get
# "<span class="list-tool-pagination-text">
# Page<!-- --> <strong>1<!-- -->/<!-- -->8</strong></span>"
# WE add the <strong tag to search and get, we seek to get out the number 8 - total pages:

page_text = doc.find(class_='list-tool-pagination-text').strong
# print(page_text)

# <strong>1<!-- -->/<!-- -->8</strong>
# We got the small piece so we need to convert everything to string, split it in two parts
# And get the part on the right
# Elements in the page_text are divided and counted by "/"
# pages = str(page_text).split('/')[-2]
# print(pages)

# <!-- -->8<
# Extracting the number, it could be 2 or 3 digit, so we need to split
# pages = str(page_text).split('/')[-2].split('>')[-1][:-1]
# print(pages)

# ['<!-- --', '8<'] we need the second element, i add up there [-1],
# And we add [:-1] to remove the "<"

# Result: 8, now we need the number to turn into an int
pages = int(str(page_text).split('/')[-2].split('>')[-1][:-1])
# print(pages)

# Enter to check other search 3070, Result 7

# So now we have all the pages we want to loop
# through all the pages and get the result

for page in range(1, pages + 1):  # We do not want ot start from page 0,
    # so set the count from 1, we add +1 because the for loop
    # Will not touch the last page
    # We add the page count
    url = f"https://www.newegg.ca/p/pl?d={search_term}&N=4131&page={page}"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")
    div = doc.find(class_='item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell')
    items = div.find_all(text=re.compile(search_term))  # Compile helps to find extended terms
    # for ex. search_term = 3080, and the product has "3080 GPU"
    # with compile it will find the item
    for item in items:
        parent = item.parent
        if parent.name != "a":
            continue
        link = parent['href']  # We want to get the links for the products
        next_parent = item.find_parent(class_="item-container")
        try:
            price = next_parent.find(class_="price-current").strong.string  # THats how we got all the prices
            items_found[item] = {"price": int(price.replace(",", "")), "link": link}
        except:
            pass

    print(items_found)

sorted_items = sorted(items_found.items(), key=lambda x: x[1]['price'])

for item in sorted_items:
    print(item[0])
    print(f"${item[1]['price']}")
    print(item[1]['link'])
    print('___________________________________')

# save result to an sqlite database
conn = sqlite3.connect('newegg.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS newegg
                (name text, price integer, link text)''')
for item in sorted_items:
    c.execute("INSERT INTO newegg VALUES (?, ?, ?)", (item[0], item[1]['price'], item[1]['link']))
conn.commit()
conn.close()



# If you look at the HTML, you can see that <item-cells-wrap border-cells
# items-grid-view four-cells expulsion-one-cell>
# Contain all search results, so we create a new variable div
# We got a lot of text, but it is better, we need to grab the href

# Lets try and sort our results by sorted

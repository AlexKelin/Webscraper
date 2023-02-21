**Webscraper Video Card Search Tool**

This is a simple Python program that allows the user to search for video card models on the Newegg website and retrieve the prices and links for the products and store the results to an SQL database.

**Requirements**

Python 3.x
requests library
BeautifulSoup library
sqlite3 library

**Usage**

Run the program by executing python video_card_search.py in the terminal.
Input the video card model you want to search for.
The program will scrape the Newegg website and retrieve the prices and links for the products.
The program will store the data in an SQLite database.

**Program Explanation**

The get_model function asks the user for the video card model they want to search for.
The get_clean_page function retrieves the number of pages and the HTML document from the Newegg website using the user's search term.
The parse_page function loops through each page of the search results, extracts the product names, links, and prices, and stores the data in a dictionary.
The store_data function creates an SQLite database and stores the data retrieved from the Newegg website.
The main function combines the above functions to provide a complete search experience for the user.

**Future Improvements**

Add error handling for invalid input or unexpected website response.
Add the ability to sort by price, rating, and other factors.
Improve database management, such as allowing users to export or import data.
Add support for additional websites or product categories.



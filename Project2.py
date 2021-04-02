from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """
    #opening the file before reading it
    with open(filename, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
    #Find the table with all the information we need
    titles = soup.find('table', {"class": "tableList"})
    #creating an empty list in which tuples will be entered
    titles_list = []
    #finding all the table rows that we will iterate through
    tr_list = titles.find_all('tr')
    for tr in tr_list:
        #finding all the table data
        td_list = tr.find_all('td')
        td_main = td_list[1]
        #searching for the title of the book then the author
        title_link = td_main.find('a', {"class": "bookTitle"})

        author_link = td_main.find('a', {"class": "authorName"})
  
        title = title_link.text.strip()
  
        author = author_link.text.strip()
        #adding everythig into a tuple
        tup = (title, author)
        titles_list.append(tup)

    return titles_list


        
    
    

    


def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """

    #requesting information from the website
    url = "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    table = soup.find('table', {"class": "tableList"})
    rows = table.find_all('tr')
    links = []
    #want all links to start with this
    start_link = "https://www.goodreads.com"
    #iterating through first 10 items
    for row in rows[:10]:
        #finding all the table data and iterating through the second one of each row because it has the relevant information
        td_list = row.find_all('td')
        td_want = td_list[1]
        #getting the link for the title
        title_link = td_want.find('a', {"class": "bookTitle"})
        end_link = title_link['href']
        #making sure the /book/show/ is in the link
        if end_link[:11] == '/book/show/':
            full_link = start_link + end_link
            links.append(full_link)

    return links



def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """

    r = requests.get(book_url)
    soup = BeautifulSoup(r.text, 'html.parser')

    title_tag = soup.find('h1', {"id": "bookTitle"})
    title = title_tag.text.strip()
    author_tag = soup.find('div', {'id': 'bookAuthors'})
    spans = author_tag.find_all('span')
    author = spans[1].text.strip()

    num_pages_tag = soup.find('span', {'itemprop': 'numberOfPages'})
    num_pages = num_pages_tag.text.strip()
    num_pages_list = num_pages.split()
    num = num_pages_list[0]
    num_pages_int = int(num)
    tup = (title, author, num_pages_int)
    return tup







def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    with open(filepath, 'r') as f:
        soup = BeautifulSoup(f,'html.parser')
    categories_section = soup.find('div',{"class": "categoryContainer"})
    categories = categories_section.find_all('div', {"class": "category clearFix"})
    best_book = []

    for category in categories:
        url_tag = category.find('a')
        url = url_tag['href']
        title_tag = category.find('h4', {"class": 'category__copy'})
        title = title_tag.text.strip()
        image_tag = category.find('img', {"class": "category__winnerImage"})
        book = image_tag['alt']
        tup = (title, book, url)
        best_book.append(tup)
    
    return best_book





def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    headers = ["Book title", "Author Name"]
    with open(filename, "w") as f:
        csv_writer = csv.writer(f, delimiter=',', quotechar='"')
        csv_writer.writerow(headers)
        for tup in data:
            csv_writer.writerow(tup)


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    pass

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    search_urls = get_search_links()

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        titles = get_titles_from_search_results('search_results.htm')
        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(titles), 20)

        # check that the variable you saved after calling the function is a list
        self.assertIsInstance(titles, list)

        # check that each item in the list is a tuple
        for item in titles:
            self.assertIsInstance(item, tuple)

        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertTrue(titles[0],"Harry Potter and the Deathly Hallows (Harry Potter, #7)")

        # check that the last title is correct (open search_results.htm and find it)
        self.assertTrue(titles[-1],"Harry Potter: The Prequel (Harry Potter, #0.5")

    def test_get_search_links(self):

        # check that TestCases.search_urls is a list
        self.assertIsInstance(TestCases.search_urls, list)
        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(TestCases.search_urls), 10)
        # check that each URL in the TestCases.search_urls is a string
        for url in TestCases.search_urls:
            self.assertIsInstance(url, str)
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
            self.assertTrue(url[:36], 'https://www.goodreads.com/book/show/')



    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        # for each URL in TestCases.search_urls (should be a list of tuples)
        tups = []
        # check that the number of book summaries is correct (10)
        for url in TestCases.search_urls:
            # check that each item in the list is a tuple
            summary = get_book_summary(url)
            tups.append(summary)
            # check that each tuple has 3 elements
        self.assertEqual(len(tups), 10)
            # check that the first two elements in the tuple are string
        for url in tups:
            # check that the third element in the tuple, i.e. pages is an int
            self.assertIsInstance(url, tuple)
            self.assertEqual(len(url),  3)
            # check that the first book in the search has 337 pages
        self.assertIsInstance(tups[0][0], str)
        self.assertIsInstance(tups[0][1], str)

        self.assertIsInstance(tups[0][2], int)

        self.assertEqual(tups[0][2], 337)


    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        best_books_tups = summarize_best_books('best_books_2020.htm')

        # check that we have the right number of best books (20)
        self.assertEqual(len(best_books_tups), 20)

            # assert each item in the list of best books is a tuple
        for item in best_books_tups:
            self.assertIsInstance(item, tuple)

            # check that each tuple has a length of 3
            self.assertEqual(len(item), 3)

        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(best_books_tups[0], ('Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'))
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(best_books_tups[-1], ('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'))


    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        data = get_titles_from_search_results('search_results.htm')
        # call write csv on the variable you saved and 'test.csv'
        write_csv(data, 'test.csv')

        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        csv_lines = []
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test.csv'), 'r') as f:
            csv_object = csv.reader(f)
            for line in csv_object:
                csv_lines.append(line)

        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_lines), 21)

        # check that the header row is correct
        self.assertEqual(csv_lines[0], ['Book title', 'Author Name'])

        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertEqual(csv_lines[0], ['Book title', 'Author Name'])

        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        self.assertEqual(csv_lines[0], ['Book title', 'Author Name'])



if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)
    




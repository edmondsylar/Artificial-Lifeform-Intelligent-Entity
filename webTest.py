import requests
from bs4 import BeautifulSoup
import requests

# search engine
class Search:
  def __init__(self, query):
    # format query
    self.query = query.replace(" ", "+")
    # construct url
    self.url = f"https://www.google.com/search?q={self.query}"
    # initialize empty dictionary for results
    self.results = {}

  def get_important_info(self):
    # make request and get response
    response = requests.get(self.url)
    soup = BeautifulSoup(response.content, "lxml")

    # extract content, headings, and links with proper filtering
    content = soup.find("main") or soup.find("article")
    if content:
      content = content.text.strip()
    headings = [h.text.strip() for h in soup.find_all(lambda tag: tag.name in ["h1", "h2", "h3"])]
    links = [a["href"] for a in soup.find_all("a") if not a.parent.has_attr("class")]

    # store extracted information in the results dictionary
    self.results["content"] = content
    self.results["headings"] = headings
    self.results["links"] = links

  def clean(self, html_output):
    soup = BeautifulSoup(html_output, "html.parser")

    # extract title and summary (can be adjusted to extract specific elements)
    self.results["title"] = soup.title.get_text()
    self.results["summary"] = soup.find("div", id="main").get_text()

  def print_results(self):
    # pretty print the results dictionary
    print(f"Title: {self.results}")
  def get_all_results(self):
    # return the complete dictionary of results
    return self.results



# create a Search object with a query
search = Search("artificial intelligence")

# get important information
search.get_important_info()

# print the results
search.print_results()

# access specific information
content = search.results["content"]
headings = search.results["headings"]

# access all results as a dictionary
all_results = search.get_all_results()

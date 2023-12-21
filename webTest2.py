from bs4 import BeautifulSoup
import requests

def get_important_info(url):
  """
  Fetches a web page, cleans the text, and returns the main content, headings, and links.

  Args:
    url: The URL of the web page to scrape.

  Returns:
    A dictionary containing the extracted information:
      * content: The main content of the page as a string.
      * headings: A list of heading texts (h1, h2, etc.).
      * links: A list of all valid links found on the page.
  """

  # Fetch the page
  response = requests.get(url)

  # Check for successful response
  if response.status_code != 200:
    raise Exception(f"Error fetching page: {response.status_code}")

  # Parse the HTML with BeautifulSoup
  soup = BeautifulSoup(response.content, "lxml")

  # Extract main content
  content = soup.find("main") or soup.find("article")
  if content:
    content = content.text.strip()

  # Extract headings
  headings = [h.text.strip() for h in soup.find_all(lambda tag: tag.name in ["h1", "h2", "h3"])]

  # Extract links (excluding menus)
  links = [a["href"] for a in soup.find_all("a") if not a.parent.has_attr("class", "menu")]

  # Return the extracted information
  return {"content": content, "headings": headings, "links": links}

# Example usage
url = "https://www.example.com/interesting-article"
info = get_important_info(url)

print(f"Content: {info['content']}")
print(f"Headings: {info['headings']}")
print(f"Links: {info['links']}")

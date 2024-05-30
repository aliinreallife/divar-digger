from typing import List
from bs4 import BeautifulSoup
import requests


def extract_links(url: str) -> List[str]:
    """
    Given a URL of a listings page, this function extracts and returns a list of URLs found within <a> tags in divs with the class 'post-list__widget-col-c1444'.

    Args:
        url (str): The URL of the listings page to scrape.

    Returns:
        List[str]: A list of URLs from the listings.
    """
    response = requests.get(url)
    urls = []

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all <a> tags within the specified parent class
        parent_divs = soup.find_all("div", class_="post-list__widget-col-c1444")
        if not parent_divs:
            print("No parent divs found")
            print(soup.prettify())
        else:
            for parent in parent_divs:
                link = parent.find("a")
                if link:
                    href = link.get("href")
                    if href:
                        href = remove_optional_part(
                            href
                        )  # in the link there is a persian part that is not necessary so we remove it
                        urls.append(f"https://divar.ir{href}")
    else:
        print("Failed to retrieve the page")

    return urls


def remove_optional_part(url: str) -> str:
    """
    Given a URL, this function removes the persian optional part that that is there for seo reasons i think.

    Args:
        url (str): The URL to process.

    Returns:
        str: The processed URL without the optional part.
    """
    base, _, last = url.rpartition("/")
    base_url = base.rpartition("/")[0]
    return f"{base_url}/{last}"

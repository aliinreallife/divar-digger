from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import requests


BASE_URL = "https://divar.ir/v/"
PARENT_CLASS = "post-list__widget-col-c1444"
TITLE_CLASS = "kt-page-title__title"
PRICE_CLASS = "kt-unexpandable-row__value"
DATA_ROW_CLASS = "kt-group-row__data-row"
GROUP_ROW_ITEM_CLASS = "kt-group-row-item"
AGENCY_CLASS = "kt-text-truncate"
IMAGE_CLASS = "kt-image-block__image"
DESCRIPTION_CLASS = "kt-description-row__text"


def extract_id_from_href(href: str) -> str:
    """
    Given a URL, this function extracts the last part of the URL which is considered as ID.

    Args:
        href (str): The URL to process.

    Returns:
        str: The ID extracted from the URL.
    """
    _, _, last = href.rpartition("/")
    return last


def extract_IDs(url: str) -> List[str]:
    """
    Given a URL of a listings page, this function extracts and returns a list of IDs found within <a> tags in divs with the class 'post-list__widget-col-c1444'.

    Args:
        url (str): The URL of the listings page to scrape.

    Returns:
        List[str]: A list of IDs from the listings.
    """
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the page")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    parent_divs = soup.find_all("div", class_=PARENT_CLASS)
    if not parent_divs:
        print("No parent divs found")
        return []

    IDs = []
    for parent in parent_divs:
        link = parent.find("a")
        if link and link.get("href"):
            id = extract_id_from_href(link.get("href"))
            IDs.append(id)

    return IDs


def extract_real_estate_data(id: str) -> Optional[Dict[str, any]]:
    """
    Given an ID of a listing, this function extracts and returns the details of the listing.

    Args:
        id (str): The ID of the listing to scrape.

    Returns:
        dict: A dictionary containing the listing details, or None if failed to load the webpage.
    """
    url = BASE_URL + id
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to load webpage: {url}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    data = {}

    # Extract the title
    title = soup.find("div", class_=TITLE_CLASS)
    if title:
        data["title"] = title.text.strip()

    # Extract the price
    price = soup.find("p", class_=PRICE_CLASS)
    if price:
        try:
            price_text = price.text.replace("٬", "").replace("تومان", "").strip()
            data["price"] = int(price_text)
        except ValueError:
            data["price"] = "Invalid price"

    # Extract property details
    data_rows = soup.find_all("tr", class_=DATA_ROW_CLASS)
    if data_rows:
        items = data_rows[0].find_all("td", class_=GROUP_ROW_ITEM_CLASS)
        if len(items) == 3:
            try:
                data["metrage"] = int(items[0].text.strip())
                year_text = items[1].text.strip()
                data["year_of_construction"] = (
                    int(year_text) if year_text.isdigit() else "Before 1370"
                )
                data["number_of_rooms"] = int(items[2].text.strip())
            except ValueError:
                data["metrage"] = data["year_of_construction"] = data[
                    "number_of_rooms"
                ] = "Invalid data"

        if len(data_rows) > 1:
            items = data_rows[1].find_all("td", class_=GROUP_ROW_ITEM_CLASS)
            if len(items) == 3:
                data["has_elevator"] = "ندارد" not in items[0].text
                data["has_parking"] = "ندارد" not in items[1].text
                data["has_storage_room"] = "ندارد" not in items[2].text

    # Extract agency and agent details
    agency = soup.find("a", class_=AGENCY_CLASS)
    if agency:
        data["agency"] = agency.text.strip()
        agency.decompose()
    agent = soup.find("a", class_=AGENCY_CLASS)
    if agent:
        data["agent"] = agent.text.strip()

    # Extract image presence
    image = soup.find("img", class_=IMAGE_CLASS)
    if data:
        data["has_image"] = bool(
            image
            and "ls-is-cached" not in image.get("class")
            and "kt-image-block__image--lazy-loaded" not in image.get("class")
        )

    # Extract the description
    description = soup.find("p", class_=DESCRIPTION_CLASS)
    if description:
        data["description"] = (
            description.text.strip() if description else "No description available"
        )

    if data:
        data["_id"] = id
    else:
        print(f"Failed to extract data from {url}")

    return data

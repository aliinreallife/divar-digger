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


def extract_real_estate_data(url: str) -> dict:
    """
    Given a URL of a listing, this function extracts and returns the title, price, and description of the listing. TODO: be more specefic

    Args:
        url (str): The URL of the listing to scrape.

    Returns:
        dict: A dictionary containing the title, price, and description of the listing.
    """
    response = requests.get(url)
    data = {}

    # Check if the request was successful
    if response.status_code == 200:

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract the title
        title = soup.find("div", class_="kt-page-title__title")
        if title:
            data["title"] = title.text.strip()

        # Extract the price
        price = soup.find("p", class_="kt-unexpandable-row__value")
        if price:
            price = price.text
            price = int(price.replace("٬", "").replace("تومان", ""))
            data["price"] = price

        # Extract the metrage, year of construction, and number of rooms
        data_row = soup.find("tr", class_="kt-group-row__data-row")
        if data_row:
            items = data_row.find_all("td", class_="kt-group-row-item")
            if items and len(items) == 3:
                metrage = int(items[0].text)
                data["metrage"] = metrage
                data["year_of_construction"] = int(items[1].text)
                data["number_of_rooms"] = int(items[2].text)
            # Remove the first occurrence
            data_row.decompose()

        # Now find the second occurrence
        data_row = soup.find("tr", class_="kt-group-row__data-row")
        if data_row:
            items = data_row.find_all("td", class_="kt-group-row-item")
            if items and len(items) == 3:
                elevator_info = items[0].text
                parking_info = items[1].text
                storage_room_info = items[2].text

                data["has_elevator"] = "ندارد" not in elevator_info
                data["has_parking"] = "ندارد" not in parking_info
                data["has_storage_room"] = "ندارد" not in storage_room_info

        agency = soup.find("a", class_="kt-text-truncate")
        if agency:
            data["agency"] = agency.text.strip()
            agency.decompose()
        agent = soup.find("a", class_="kt-text-truncate")

        if agent:
            data["agent"] = agent.text.strip()

        image = soup.find("img", class_="kt-image-block__image")
        if image:
            if "ls-is-cached" not in image.get(
                "class"
            ) and "kt-image-block__image--lazy-loaded" not in image.get("class"):
                data["has_image"] = True
            else:
                data["has_image"] = False

        location = soup.find("div", class_="map-cm--padded")
        if location:
            data["has_location"] = True
        elif data:
            data["has_location"] = False

        # Extract the description
        description = soup.find("p", class_="kt-description-row__text")
        if description:
            pass
            # data["description"] = description.text.strip()

    if data:
        data["link"] = url
    else:
        print("faild to load webpage:", url)

    return data


url = "https://divar.ir/v/QZAH5ALG"
data = extract_real_estate_data(url)

for key, value in data.items():
    print(f"{key}: {value}")

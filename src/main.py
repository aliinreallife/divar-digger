from typing import List
from keeper.keeper import insert_data, is_id_in_database
from crawler.crawler import extract_real_estate_data, extract_IDs


def blah(listings_page_url: str = "https://divar.ir/s/lavasan/buy-apartment"):

    IDs: List = extract_IDs(listings_page_url)
    for id in IDs:
        if not is_id_in_database(id, collection=listings_page_url):
            print(f"Processing item: {id}")
            data = extract_real_estate_data(id)
            if data:
                insert_data(data, collection=listings_page_url)
        else:
            print(f"Item {id} already exists in the database, skipping.")

blah()
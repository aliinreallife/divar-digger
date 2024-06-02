from time import sleep
from typing import List

from tqdm import tqdm

from crawler.crawler import extract_IDs, extract_real_estate_data
from keeper.keeper import insert_data, is_id_in_database


def blah(
    listings_page_url: str = "https://divar.ir/s/lavasan/buy-apartment",
    max_retries: int = 16,
):
    retries = 0

    while retries < max_retries:
        IDs: List[str] = extract_IDs(listings_page_url)

        if IDs:
            for id in tqdm(IDs, desc="Processing items"):
                if not is_id_in_database(id, collection_name=listings_page_url):
                    print(f"Processing item: {id}")
                    data = extract_real_estate_data(id)
                    if data:
                        insert_data(data, collection_name=listings_page_url)
                    else:
                        print(f"Failed to extract data for item {id}, skipping.")
                else:
                    print(f"Item {id} already exists in the database, skipping.")
            return  # Exit function after successful processing

        else:
            retries += 1
            print(f"Failed to retrieve the page, retrying ({retries}/{max_retries})...")
            sleep(4)

    print(f"Failed to process after {max_retries} retries.")


blah()

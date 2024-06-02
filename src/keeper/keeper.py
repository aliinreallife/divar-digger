from typing import Any, Dict

from pymongo import MongoClient


def insert_data(data: Dict[str, Any]) -> bool:
    """
    Given a dictionary of data, this function inserts the data into a MongoDB database.

    Args:
        data (dict): A dictionary containing the data to insert.

    Returns:
        bool: True if the data was inserted successfully, False otherwise.
    """
    # Create a connection to the MongoDB database
    client = MongoClient("mongodb://localhost:27017/")

    # Access the database
    db = client["real_estate_data"]

    # Access the collection
    collection = db["listings"]

    # Check if a document with the same link already exists
    existing_document = collection.find_one({"link": data["link"]})

    if existing_document is None:
        # Insert the data into the collection
        collection.insert_one(data)
        print("Data inserted successfully")
        return True
    else:
        print("Data already exists in the database")
        return False

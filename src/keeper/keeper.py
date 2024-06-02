from typing import Any, Dict

from pymongo import MongoClient

# Create a connection to the MongoDB database
client = MongoClient("mongodb://localhost:27017/")

# Access the database
db = client["real_estate_data"]  # TODO: make it more flexible


def insert_data(data: Dict[str, Any], collection_name) -> bool:
    """
    Given a dictionary of data, this function inserts the data into a MongoDB database.

    Args:
        data (dict): A dictionary containing the data to insert.
    """
    # Access the collection
    collection = db[collection_name]

    collection.insert_one(data)


def is_id_in_database(id, collection_name) -> bool:
    """this function checks if a document with the given id exists in the database
    Args:
        id (str): the id of the document
        collection_name (str): the name of the collection

    Returns:
        bool: True if the document exists, False otherwise
    """
    # Access the collection
    collection = db[collection_name]
    existing_document = collection.find_one({"_id": id})
    return existing_document is not None

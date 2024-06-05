from os import getenv
from typing import Any, Dict

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongodb_host_port = getenv("MONGODB_HOST_PORT")
mongodb_connection_string = f"mongodb://{mongodb_host_port}/"

# Create a connection to the MongoDB database
client = MongoClient(mongodb_connection_string)

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

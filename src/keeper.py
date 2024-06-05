from os import getenv
from typing import Any, Dict

from dotenv import load_dotenv
from pymongo import MongoClient, errors

load_dotenv()

mongodb_host_port = getenv("MONGODB_HOST_PORT")
mongodb_local_connection_string = f"mongodb://{mongodb_host_port}/"

# Create a connection to the local MongoDB database
local_client = MongoClient(mongodb_local_connection_string)

# Access the local database
local_db_name = getenv("MONGODB_LOCAL_DB_NAME", "real_estate_data")
local_db = local_client[local_db_name]

mongodb_online_connection_string = getenv("MONGODB_ONLINE_CONNECTION_STRING")

# Create a connection to the online MongoDB database
online_db = None
if mongodb_online_connection_string:
    try:
        online_client = MongoClient(
            mongodb_online_connection_string, serverSelectionTimeoutMS=5000
        )
        online_client.server_info()  # Will raise ServerSelectionTimeoutError if server is not available
        online_db_name = getenv("MONGODB_ONLINE_DB_NAME", "real_estate_data")
        online_db = online_client[online_db_name]
    except errors.ServerSelectionTimeoutError:
        print("Failed to connect to the online database.")
else:
    print("No online database connection string provided.")


def insert_data(data: Dict[str, Any], collection_name: str) -> bool:
    """
    Given a dictionary of data, this function inserts the data into a MongoDB database.

    Args:
        data (dict): A dictionary containing the data to insert.
        collection_name (str): The name of the collection to insert the data into.
    """
    # Access the local and online collections
    local_collection = local_db[collection_name]
    local_collection.insert_one(data)

    if online_db:
        online_collection = online_db[collection_name]
        online_collection.insert_one(data)


def is_id_in_database(id: str, collection_name: str) -> bool:
    """
    This function checks if a document with the given id exists in the database.

    Args:
        id (str): The id of the document.
        collection_name (str): The name of the collection.

    Returns:
        bool: True if the document exists, False otherwise.
    """
    # Access the collection
    local_collection = local_db[collection_name]
    existing_document = local_collection.find_one({"_id": id})
    return existing_document is not None

from pymongo import MongoClient


def save_to_mongodb(data_list, uri, db_name="IPEnrichment", collection_name="AbuseVT"):
    """
    Saving VT data to database
    :param data_list: VT data
    :param uri: connection String
    :param db_name: Database name
    :param collection_name: Collection name
    :return: None
    """
    try:
        client = MongoClient(uri)
        db = client[db_name]
        collection = db[collection_name]
        collection.insert_many(data_list)
    except Exception as err:
        print(f"Exception occurred during db ingestion. ERROR: {err}")

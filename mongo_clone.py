import pymongo
import json
import os
from datetime import datetime

def backup_mongodb(source_uri, backup_dir):
    """Backs up all databases, collections, and documents to a local directory, including system dbs."""

    print(f"Starting backup from: {source_uri}")
    client = pymongo.MongoClient(source_uri)

    try:
        os.makedirs(backup_dir, exist_ok=True)

        db_names = client.list_database_names()

        if not db_names:
            print("No databases to backup. Exiting.")
            return

        print(f"Databases to backup: {', '.join(db_names)}")

        for db_name in db_names:
            db = client[db_name]
            print(f"Backing up database: {db_name}")

            for collection_name in db.list_collection_names():
                print(f"  Backing up collection: {collection_name}")

                collection = db[collection_name]
                documents = list(collection.find())

                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                filename = os.path.join(backup_dir, f"{db_name}_{collection_name}_{timestamp}.json")

                with open(filename, 'w') as f:
                    json.dump(documents, f, default=str, indent=4)

                print(f"  Collection '{collection_name}' backed up to: {filename}")

    except pymongo.errors.ConnectionFailure as e:
        print(f"Error connecting to MongoDB source: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during backup: {e}")
    finally:
        client.close()
        print("Backup process finished.")

def restore_mongodb(target_uri, backup_dir):
    """Restores data from backup files to the target MongoDB server, excluding system dbs."""

    print(f"Starting restore to: {target_uri}")
    client = pymongo.MongoClient(target_uri)

    try:
        if not os.path.exists(backup_dir):
            print(f"Backup directory not found: {backup_dir}")
            return

        print(f"Scanning directory: {backup_dir}")
        backup_files = [f for f in os.listdir(backup_dir) if f.endswith(".json")]

        if not backup_files:
            print(f"No backup files found in: {backup_dir}")
            return

        for filename in backup_files:
             try:
                parts = filename.split("_")
                if len(parts) != 3:
                    print(f"Skipping invalid filename {filename} expected <database_name>_<collection_name>_<timestamp>.json")
                    continue

                db_name = parts[0]
                collection_name = parts[1]

                if db_name == 'admin' and collection_name == 'system.version':
                    print(f"Skipping restoring collection {collection_name} in db {db_name}, system collection.")
                    continue

                if db_name == 'local':
                    print(f"Skipping restoring db {db_name}, system database.")
                    continue

                print(f"Restoring collection {collection_name} in db {db_name}")

                filepath = os.path.join(backup_dir, filename)

                with open(filepath, "r") as f:
                    documents = json.load(f)

                if len(documents) == 0:
                    print(f"Collection {collection_name} in db {db_name} was empty")
                    continue

                db = client[db_name]
                collection = db[collection_name]

                collection.insert_many(documents)
                print(f"  Restored {len(documents)} documents into: {db_name}.{collection_name}")
             except Exception as e:
                    print(f"Error restoring file {filename} error: {e}")


    except pymongo.errors.ConnectionFailure as e:
        print(f"Error connecting to MongoDB target: {e}")
    except FileNotFoundError:
        print(f"Error: could not find the backup directory: {backup_dir}")
    except Exception as e:
        print(f"An unexpected error occurred during restore: {e}")
    finally:
        client.close()
        print("Restore process finished.")

if __name__ == "__main__":
    source_connection_string = "mongodb://192.168.1.116:27017"
    target_connection_string = "mongodb://127.0.0.1:27017"
    backup_directory = "./mongodb_backup"

    backup_mongodb(source_connection_string, backup_directory)
    restore_mongodb(target_connection_string, backup_directory)
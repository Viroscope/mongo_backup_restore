```markdown
# MongoDB Backup and Restore Utility

This Python script provides a simple utility to backup and restore MongoDB databases. It allows you to backup all databases, collections, and documents from a source MongoDB server to a local directory, and then restore them to a target MongoDB server.

## Features

*   **Backup**: Backs up all databases (including system databases), collections, and documents from a source MongoDB server to a local directory.
*   **Restore**: Restores data from backup files to a target MongoDB server.
*   **JSON Format**: Backups are stored as JSON files, making them human-readable and easy to inspect.
*   **Timestamped Backups**: Each collection backup is timestamped, preventing filename collisions.
*   **Error Handling**: Includes error handling for connection failures, file issues, and unexpected exceptions.
*   **System Database Exclusion**: The restore process skips the 'local' database and 'admin.system.version' collection.

## Prerequisites

*   Python 3.6+
*   pymongo library: Install with `pip install pymongo`

## Usage

### 1. Clone the repository or download the script

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

### 2. Configure connection strings and backup directory

   Modify the `if __name__ == "__main__":` section to match your setup:

   ```python
   if __name__ == "__main__":
        source_connection_string = "mongodb://<source_mongodb_host>:<source_mongodb_port>"  # Example: "mongodb://192.168.1.116:27017"
        target_connection_string = "mongodb://<target_mongodb_host>:<target_mongodb_port>" # Example: "mongodb://127.0.0.1:27017"
        backup_directory = "./mongodb_backup"
        
        backup_mongodb(source_connection_string, backup_directory)
        restore_mongodb(target_connection_string, backup_directory)
    ```

   *   Replace `<source_mongodb_host>` and `<source_mongodb_port>` with your source MongoDB server's hostname or IP address and port.
   *   Replace `<target_mongodb_host>` and `<target_mongodb_port>` with your target MongoDB server's hostname or IP address and port.
   *   The `backup_directory` specifies where backup files will be stored, change it as needed.

### 3. Run the script

   ```bash
   python <script_name>.py
   ```
   Replace `<script_name>.py` with the name of your python script file.

### 4. Backup process

   *   The script will create a directory named after `backup_directory` if it doesn't exist.
   *   It will connect to the source MongoDB server.
   *   For each database, collection and document it will create a json file in the format `<database_name>_<collection_name>_<timestamp>.json`

### 5. Restore process

   *   The script will connect to the target MongoDB server.
   *   It will read all json files in the backup directory
   *   For each file that matches the pattern `<database_name>_<collection_name>_<timestamp>.json`, it will restore the content in the corresponding database and collection
   * It skips restoring the `local` database and the `admin.system.version` collection, since they are system collections and should not be restored.

## Important Considerations

*   **Authentication**: The script does not handle authentication. If your MongoDB servers require authentication, you'll need to include that in your connection strings or use a user with appropriate permissions.
*   **Large Databases**: For large databases, this script might be slow and consume a lot of memory since the backup process loads the entire collection into memory. Consider using MongoDB's built-in tools like `mongodump` and `mongorestore` for large datasets, which can be more efficient.
*   **System Databases**: The restore process does not restore system databases, specifically the 'local' database and the 'admin.system.version' collection. This is intentional as these databases usually do not contain user data and restoring them can cause issues.
*   **Error Handling**: The script includes basic error handling, but it's recommended to monitor the output of the script for any error messages.
*   **Permissions**: Ensure the script has the necessary permissions to create the backup directory and read/write the JSON files within it.
*   **Data Loss**: Always test the backup and restore process in a development environment before applying it to production to prevent accidental data loss or corruption.
*   **JSON Encoding**:  The script uses `json.dump(documents, f, default=str, indent=4)` which handles encoding of objects that are not json encodable by default.

## Potential Improvements

*   Implement authentication for MongoDB connections.
*   Add support for incremental backups.
*   Implement a progress indicator for large backups/restores.
*   Explore using `mongodump`/`mongorestore` from within the script for better performance and efficiency with large datasets.
*   Consider adding a config file instead of hardcoding the connection strings and backup directory.
*   Add command-line argument parsing to the script using `argparse`.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
```



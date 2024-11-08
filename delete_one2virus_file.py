import os

# Specify the name of the file to delete and the root directory to search
target_file = "Open Notebook.onetoc2"
root_folder = r"D:/Mydataadd/bitcoin_killer"
log_file = "deletion_log.txt"

# Open the log file to record results
with open(log_file, "w") as log:
    log.write(f"Searching for '{target_file}' in '{root_folder}' and deleting all occurrences...\n\n")

    # Walk through each directory and subdirectory
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename == target_file:
                file_path = os.path.join(dirpath, filename)
                try:
                    # Attempt to delete the file
                    os.remove(file_path)
                    log.write(f"Successfully deleted: {file_path}\n")
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    # Log any issues if the file could not be deleted
                    log.write(f"Failed to delete: {file_path}. Reason: {e}\n")
                    print(f"Failed to delete: {file_path}. Reason: {e}")

print("Deletion process completed. Check 'deletion_log.txt' for details.")

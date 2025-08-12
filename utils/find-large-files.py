import os
import sys

def list_files_in_folder(folder_path):
    """
    Lists files in a given folder and its subdirectories, sorted by size in descending order.

    Args:
        folder_path: The path to the folder.

    Returns:
        A list of tuples, where each tuple contains the file path and its size in MB.
    """

    file_list = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                size_in_bytes = os.path.getsize(file_path)
                size_in_mb = size_in_bytes / (1024 * 1024)
                file_list.append((file_path, size_in_mb))
            except OSError as e:
                print(f"Error accessing file {file_path}: {e}", file=sys.stderr)

    # Sort by size in descending order
    file_list.sort(key=lambda x: x[1], reverse=True)
    return file_list

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python find-large-files.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]

    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a valid directory.")
        sys.exit(1)

    files = list_files_in_folder(folder_path)

    for file_path, size_in_mb in files:
        print(f"{file_path}, {size_in_mb:.2f} MB")
import os
import zipfile

def _read_files_recursively(directory: str) -> list:
    """
    Helper function to read files recursively from a directory.

    Parameters:
    directory (str): Path to the directory.

    Returns:
    list: List of file paths.
    """
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths

def read_files_from_zip(zip_path: str, extract_path: str) -> list:
    """
    Read files from a zip archive to an extract path

    Parameters:
    zip_path (str): Path to the zip file.
    extract_path (str): Path to extract contents.

    Returns:
    list: List of file paths inside the zip archive.
    """
    # Create the extraction directory if it does not exist
    os.makedirs(extract_path, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
        return _read_files_recursively(extract_path)

def read_files_from_directory(directory: str) -> list:
    """
    Read files from a directory.

    Parameters:
    directory (str): Path to the directory.

    Returns:
    list: List of file paths inside the directory.
    """
    return _read_files_recursively(directory)

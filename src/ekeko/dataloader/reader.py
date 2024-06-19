import os
import zipfile

def _read_files_recursively(directory):
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

def read_files_from_zip(zip_path):
    """
    Read files from a zip archive.

    Parameters:
    zip_path (str): Path to the zip file.

    Returns:
    list: List of file paths inside the zip archive.
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        extract_path = os.path.splitext(zip_path)[0]  # Extract to a folder with the same name as the zip file
        zip_ref.extractall(extract_path)
        return _read_files_recursively(extract_path)

def read_files_from_directory(directory):
    """
    Read files from a directory.

    Parameters:
    directory (str): Path to the directory.

    Returns:
    list: List of file paths inside the directory.
    """
    return _read_files_recursively(directory)

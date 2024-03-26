import os


def get_repo_root():
    """
    Function to find the root location of the current git repository folder.

    Returns
    -------
    file_path: str
               The root location of the git repository
    """
    file_path = os.path.abspath(__file__)
    while not os.path.exists(os.path.join(file_path, ".git")):
        if file_path == os.path.dirname(file_path):
            return ""
        file_path = os.path.dirname(file_path)

    return file_path

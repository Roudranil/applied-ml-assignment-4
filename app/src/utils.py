import os


def get_repo_root():
    """
    Function to find the root location of the current git repository folder.

    Returns
    -------
    file_path:  str
                The root location of the git repository
    """
    file_path = os.path.abspath(__file__)
    while not os.path.exists(os.path.join(file_path, ".git")):
        if file_path == os.path.dirname(file_path):
            return ""
        file_path = os.path.dirname(file_path)

    return file_path


def get_project_root():
    """
    Function to find the root location of the current project.
    This may or may not be the same as the root location of the current repo.
    This is generally the location of the first folder containing a README.md.

    Returns
    -------
    file_path:  str
                The root location of the project directory
    """
    file_path = os.path.abspath(__file__)
    while not os.path.exists(os.path.join(file_path, "README.md")):
        if file_path == os.path.dirname(file_path):
            return ""
        file_path = os.path.dirname(file_path)

    return file_path

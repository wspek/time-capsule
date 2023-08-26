import os


def file_exists_on_disk(directory, filename):
    for file in os.listdir(directory):
        root, ext = os.path.splitext(file)
        if root == filename:
            return True
    return False

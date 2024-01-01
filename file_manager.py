import os
import pickle
from typing import Any


class FileManager(object):
    def __init__(self):
        pass

    @staticmethod
    def save_pickle(obj: Any, to_filename: str, quiet: bool = True) -> None:
        """Writes a pickled representation of given Python object to the file object created from given filename.
        :param obj: Python object to save.
        :param to_filename: file name to save `obj`.
        :param quiet: output verbosity.
        """
        if obj is None:
            return
        if not quiet:
            print(f"Saving to filename: {to_filename}")
        with open(to_filename, "wb") as file:
            pickle.dump(obj, file)

    @staticmethod
    def load_pickle(from_file: str, quiet: bool = True) -> Any:
        """Loads a Python object from given filename.
        :param from_file: file name to load Python object from.
        :param quiet: output verbosity.
        """
        if FileManager.file_exists(from_file) is False:
            if not quiet:
                print(f"File {from_file} does not exist.")
            return None
        if not quiet:
            print(f"Loading from filename: {from_file}")
        with open(from_file, "rb") as index_file:
            file_content = pickle.load(index_file)
        return file_content

    @staticmethod
    def file_exists(filepath: str) -> None:
        """Checks if filepath exists.
        :param filepath: file path
        """
        return os.path.exists(filepath)

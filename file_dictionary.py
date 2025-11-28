from file import File
from typing import List

class FileDictionary():
    def __init__(self) -> None:
        self.files = {}

    def __contains__(self, file_id: str) -> bool:
        """Checks if a file with the given ID exists in the collection."""
        return file_id in self.files

    def set(self, files: List[File]):
        """Sets the files in the collection."""
        self.files = {file.id: file for file in files}

    def add(self, file: File):
        """Adds a file to the collection."""
        self.files[file.id] = file

    def remove(self, file_id: str):
        """Removes a file from the collection by its ID."""
        if file_id in self.files:
            del self.files[file_id]

    def get(self, file_id: str) -> File:
        """Retrieves a file from the collection by its ID."""
        if file_id not in self.files:
            raise ValueError(f"File with id {file_id} not found.")
        return self.files[file_id]
    
    def __str__(self) -> str:
        return "\n".join([str(file) for file in self.files.values()])

file_dict= FileDictionary()

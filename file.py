import os
from pydantic import BaseModel, Field
from setup_directory import construct_file_path

class File(BaseModel):
    id: str = Field(..., description="Reference ID of the file within the agent's context window (currently the path)")
    name: str = Field(..., description="Name of the file")
    path: str = Field(..., description="Path of the file")
    size: int = Field(..., description="Size of the file in bytes")
    content_type: str = Field(..., description="MIME type of the file")

    def get_content(self) -> str:
        with open(construct_file_path(self.path), "r") as f:
            return f.read()

    @classmethod
    def new_file(cls, path, content_type=""):
        working_path = construct_file_path(path)
        return cls(
            id=f"file:{path}",
            name=path.split("/")[-1],
            path=path,
            size=os.path.getsize(working_path),
            content_type=content_type
        )

    def __str__(self) -> str:
        return self.id

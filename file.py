from pydantic import BaseModel, Field

class File(BaseModel):
    id: str = Field(..., description="Reference ID of the file within the agent's context window (currently the path)")
    name: str = Field(..., description="Name of the file")
    path: str = Field(..., description="Path of the file")
    content: str = Field(..., description="Content of the file")
    size: int = Field(..., description="Size of the file in bytes")
    content_type: str = Field(..., description="MIME type of the file")

    def get_content(self) -> str:
        return self.content

    @classmethod
    def new_file(cls, path, content, content_type=""):
        return cls(
            id=f"file:{path}",
            name=path.split("/")[-1],
            path=path,
            content=content,
            size=len(content.encode('utf-8')),
            content_type=content_type
        )

    def __str__(self) -> str:
        return self.id

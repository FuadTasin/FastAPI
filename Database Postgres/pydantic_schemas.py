from typing import Annotated, Optional
from pydantic import BaseModel, Field
from starlette.responses import Content

class CreatePost(BaseModel):
    title:Annotated[str,Field(...,description="Title of the Post")]
    content:Annotated[str,...,Field(...,description="Title of the Post")]

class UpdatePost(BaseModel):
    title:Annotated[str,Optional()]
    Content:Annotated[str,Optional()]
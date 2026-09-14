from typing import Annotated, Optional
from pydantic import BaseModel, Field,EmailStr
from starlette.responses import Content

class CreatePost(BaseModel):
    title:Annotated[str,Field(...,description="Title of the Post")]
    content:Annotated[str,...,Field(...,description="Title of the Post")]

class UpdatePost(BaseModel):
    title:Optional[str]=Field(default=None)
    Content:Optional[str]=Field(default=None)

class CreateUser(BaseModel):
    email:EmailStr=Field(description="Email of the user")
    username:Annotated[str,"username of the user"]
    firstname:Annotated[str,"firstname of the user"]
    lastname:Annotated[str,"lastname of the user"]
    password:Annotated[str,"Password of the user"]
    role:Annotated[str,"Role of the user"]
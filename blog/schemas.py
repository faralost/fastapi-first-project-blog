from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    text: str


class Blog(BlogBase):
    title: str
    text: str

    class Config:
        orm_mode = True


class UserDetail(BaseModel):
    id: int
    name: str
    email: str
    blogs: list[Blog]

    class Config:
        orm_mode = True


class BlogDetail(Blog):
    author: UserDetail

    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str

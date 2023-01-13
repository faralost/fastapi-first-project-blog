from pydantic import BaseModel, EmailStr


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
    email: EmailStr
    blogs: list[Blog]

    class Config:
        orm_mode = True


class UserDetailInBlog(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True


class BlogDetail(Blog):
    author: UserDetailInBlog

    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    email: EmailStr
    password: str


class Login(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None

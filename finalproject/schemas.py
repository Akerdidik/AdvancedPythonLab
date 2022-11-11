from pydantic import BaseModel


class ProjectBase(BaseModel):
    project_title: str
    project_description: str


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    project_id: int
    project_owner: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    handle: str
    full_name: str
    id: int


class UserCreate(UserBase):
    password: str


class User(UserBase):
    user_id: int
    user_projects: list[Project] = []


    class Config:
        orm_mode = True

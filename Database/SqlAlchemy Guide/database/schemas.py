from typing import List

from pydantic import BaseModel


class Child_Base(BaseModel):
    c_id: int
    cname: int
    parent_id: int

    class Config:
        orm_mode = True


class Parent_Base(BaseModel):
    p_id: int
    pname: str
    # childs: List[Child_Base] = []

    class Config:
        orm_mode = True

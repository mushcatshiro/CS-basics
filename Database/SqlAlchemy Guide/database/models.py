from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from .database import Base


ONE_TO_MANY = True
MANY_TO_MANY = True
ONE_TO_ONE = True


# one to many example
class Parent(Base):
    __tablename__ = "parent"

    p_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    children = relationship("Child", back_populates="parents")

    def __repr__(self):
        return '<pname %r, children %r>' % self.pname % self.children


class Child(Base):
    __tablename__ = "child"

    c_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    p_id = Column(Integer, ForeignKey("parent.p_id"))

    parents = relationship("Parent", back_populates="children")


# association table (variable)

# association_table = Table('association', Base.metadata,
#     Column('p_id', Integer, ForeignKey('parent.p_id')),
#     Column('c_id', Integer, ForeignKey('child.c_id'))
# )

# class Parent(Base):
#     __tablename__ = "parent"

#     p_id = Column(Integer, primary_key=True, index=True)
#     pname = Column(String, unique=True, index=True)

#     children = relationship("Child",
#                             secondary=association_table,
#                             back_populates="parents")


# class Child(Base):
#     __tablename__ = "child"

#     c_id = Column(Integer, primary_key=True, index=True)
#     cname = Column(String, index=True)

#     parents = relationship("Parent",
#                            secondary=association_table,
#                            back_populates="children")

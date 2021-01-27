from database.database import SQLALCHEMY_DATABASE_URL, engine, SessionLocal
from database.schemas import Parent_Base, Child_Base
import database.models as models
from random_data_generator import RDG

import os
import sqlite3 as s
from sqlalchemy.orm import Session
from typing import List, Generator


class TestInstance:
    """
    docstring for TestInstance
    """

    def __init__(self,
                 URL: str = None,
                 SETUP: bool = False,
                 RESET: bool = False):
        self.url = URL
        self.fname = "sql_app.db"
        SETUP and self.setup_database()
        RESET and self.reset_database()
        # assume drop means just empty out tables

    @staticmethod
    def get_db() -> Generator:
        try:
            db = SessionLocal()
            yield db
        finally:
            db.close()

    def reset_database(self):
        conn = self.make_connection()
        with conn:
            cur = conn.cursor()
            tables = list(cur.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            ))
            for table in tables:
                cur.execute("DELETE FROM %s;" %table)

    def setup_database(self):
        try:
            os.remove(self.fname)
            models.Base.metadata.create_all(bind=engine)
            conn = self.make_connection()
            with conn:
                cur = conn.cursor()
                resp = cur.execute("SELECT name FROM sqlite_master" +
                                   " WHERE type ='table'" +
                                   " AND name NOT LIKE 'sqlite_%';").fetchall()
                print(resp)
        except Exception as e:
            print(e)
        finally:
            print('done creating')

    def make_connection(self):
        try:
            conn = s.connect(self.fname)
            return conn
        except Exception as e:
            print(e)

    def insert_all_one_by_one(
        self,
        db: Session = None,
        parents: List[Parent_Base] = None,
        childrens: List[Child_Base] = None
    ):
        """
        ONE to MANY
        assuming we are inserting parents WITHOUT childrens
        p1, c1, c2
        """
        for parent in parents:
            db_parent = models.Parent(**parent)
            db.add(db_parent)
            db.commit()
            db.refresh(db_parent)
            print(db_parent)
            # return the p_id here will help
            # else hard code it for this example...
        for child in childrens:
            db_child = models.Child(**child)
            db.add(db_child)
            db.commit()
            db.refresh(db_child)
            print(db_child)
        try:
            p1 = db.query(models.Parent).first()
            print(p1.children)
        except Exception as e:
            print(e)
        return

    def insert_all_by_once(
        self,
        db: Session = None,
        parents: List[Parent_Base] = None,
    ):
        """
        ONE to MANY
        assuming we are inserting parents WITH childrens
        p1 will have c1 and c2
        if (p2 will also have c1 and c2) this is not one to many relation
        """
        for parent in parents:
            db_parent = models.Parent(
                name=parent['name'],
                children=[models.Child(**c) for c in parent['children']]
            )
            db.add(db_parent)
            db.commit()
            db.refresh(db_parent)
            print(db_parent)
        try:
            parent_list = db.query(models.Parent).all()
            for parent in parent_list:
                print(parent.children)
            ass = db.query(models.association_table).all()
            print(ass)
        except Exception as e:
            print(e)
        return

    def insert_additional_child(self, child: Child_Base):
        """
        expected behavior
        insert additional child with both parents
        """
        pass

    def delete_parent(self):
        """
        expected behavior
        delete one parent all child also be deleted
        """
        pass

    def delete_child(self):
        """
        expected behavior
        delete one child all parent remains
        """
        pass


def obj_creator():
    r = RDG(["name"])
    p1 = r()
    p2 = r()
    c1 = r()
    c2 = r()
    c3 = r()

    p1['children'] = [c1, c2]
    p2['children'] = [c1, c2]
    c3['parent'] = [p1, p2]
    # c1['p_id'] = 1
    # c2['p_id'] = 1
    return p1, p2, c1, c2, c3


p1, p2, c1, c2, c3 = obj_creator()
t = TestInstance(URL=SQLALCHEMY_DATABASE_URL, SETUP=True)
t.insert_all_by_once(db=SessionLocal(), parents=[p1, p2])

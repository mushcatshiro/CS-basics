from sqlalchemy.orm import Session

from . import models, schemas


# below shows how to insert one by one
def get_parent(db: Session, p_id: int):
    return db.query(models.Parent).filter(models.Parent.p_id == p_id).first()


def create_parent(db: Session, parent: schemas.Parent_Base):
    db_parent = models.Parent(**parent.dict())
    db.add(db_parent)
    db.commit()
    db.refresh(db_parent)
    return db_parent


def get_child(db: Session, c_id: int):
    return db.query(models.Child).filter(models.Child.c_id == c_id).first()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

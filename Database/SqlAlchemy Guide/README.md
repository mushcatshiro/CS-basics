[TOC]
# SqlAlchemy Guide

## on Many-to-Many relationship

### on inserting

## on One-to-Many relationship

its relatively straight forward by ensuring the parent class id or other identifier is being used as a foreign key in the child class and state the relationship properly will do

### on inserting

```python
association_table = ''
db.add_all()
```

## on backref vs back_populates

essentially its the same, using back_populates ensure both classes indicates the relation properly, while using backref we will only have the relation declared on one of the classes

## association table (variable) vs association object (actual db object)? 
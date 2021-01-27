[TOC]
# SqlAlchemy Guide

## on Many-to-Many relationship

### on inserting

one option would be to separately update the association table.

```python
>> statement = association_table.insert().values(**values)
>> db.session.execute(statement)
>> db.session.commit()
```

## on One-to-Many relationship

its relatively straight forward by ensuring the parent class id or other identifier is being used as a foreign key in the child class and state the relationship properly will do.

### on inserting

it would be much easier to first insert parent then insert the children (if possible) something like below would work fine. no additional setup required on the database models.

```python
>> parent_id = insert_parent(**Parent_Input)
>> insert_child(**Child_Input, parent_id=parent_id)
```

if we would like to insert parent with a list of children as shown below, an association table would help.

```python
{
    "name": 'p1',
    "children" [
        {
            "name": "c1",
        },
        {
            "name": "c2",
        }
    ]
}
```

## on backref vs back_populates

essentially its the same, using back_populates ensure both classes indicates the relation properly, while using backref we will only have the relation declared on one of the classes.

> relationship.back_populates - alternative form of backref specification.

[official documentation](https://docs.sqlalchemy.org/en/13/orm/relationship_api.html#sqlalchemy.orm.backref)

## association table vs association object? 

association table is an actual table that will be created. the only difference is that if we needed extra data on the association table then we create an association object and reference it as usual.
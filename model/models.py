from sqlalchemy import Column, String,Integer,ForeignKey
# from flask_sqlalchemy import alchemy
from app import dataBase
from sqlalchemy.orm import sessionmaker, relationship


class User(dataBase.Model):
    __tablename__= 'user'
    id = Column(Integer,primary_key=True)
    public_id = Column(String(50), unique=True)
    name = Column('name', String(30))
    email=Column('email', String(30))
    age=Column('age', String(30))
    password=Column('password', String(255))
    # item=relationship('Item',backref='user')
    
    def __init__(self,public_id ,name, email, age, password):
        self.name = name
        self.public_id=public_id
        self.email = email
        self.age = age
        self.password = password

class Item(dataBase.Model):
    __tablename__='item'
    id = Column(Integer,primary_key=True)
    Categories= Column("categories",String(30))
    NameOfItem = Column("nameofitem",String(30))
    Location = Column("location",String(30))
    DescriptionOfItem = Column("description",String(30))
    Date = Column("date",String(30))
    PicOfItem = Column("picpath",String(30))
    user_id = Column(Integer)
    # user_id= Column(ForeignKey('user.id'))
from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy import create_engine, ForeignKey, Column,DateTime ,Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

## SQLalchemy
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    id = Column(Integer,primary_key=True)
    name = Column(String)
    role = Column(String) 
    compose = Column(String,unique=True)
    def __init__(self,name,role,compose):
        self.name = name
        self.role = role  
        self.compose = compose 
        
    def __repr__(self):
        return f"Category : {self.name} -- {self.role}"

class Category(db.Model):
    __tablename__ = 'category'

    id = Column(Integer,primary_key=True)
    name = Column(String,unique=True)

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return f"Category : {self.id} -- {self.name}"


class Article(db.Model):
    __tablename__ = 'articles'
    #title
    id = Column(Integer,primary_key=True)
    title = Column(String)
    category = db.Column(Integer,ForeignKey('category.id'))
    banner = db.String()
    #created_at = db.Column(db.DateTime(timezone=True), server_default=datetime.)
    #updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    author_id = db.Column(Integer,ForeignKey('authors.id'))
    

    def __init__(self,title,category):
        self.title = title 
        self.category = category    

    def __repr__(self):
        return f"Article : {self.title} -- {self.created_at}"
    

class Section(db.Model):
    __tablename__ = "sections"

    id = Column(Integer,primary_key=True)
    heading = Column(String) #h2 only
    text = Column(String)
    image_path = Column(String) # contain the path
    article = Column(Integer,ForeignKey('articles.id'))
    
    def __init__(self,text,heading,image_path,article):
        self.text = text
        self.heading = heading
        self.article = article
        self.image_path = image_path  

    def __repr__(self):
        return f"Section : {self.id}"

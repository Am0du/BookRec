
from sqlalchemy import Column, Integer, String, Text
from models.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import uuid


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(250), nullable=False)
    about = Column(Text, nullable=True)
    name = Column(String(250), nullable=False)
    books = relationship('Books', back_populates='author')

    def __init__(self, email, password, about, name):
        # self.id = uuid.uuid4().int
        self.email = email
        self.password = password
        self.about = about
        self.name = name



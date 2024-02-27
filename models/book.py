from models.database import Base
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Books(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    genre = Column(String(250), nullable=False)
    author_id = Column(Integer, ForeignKey('author.id'))
    author = relationship('Author', back_populates='books')


    def __init__(self, title: str, description: str, genre: str, author: int):
        self.title = title
        self.description = description
        self.genre = genre
        self.author_id = author

    # def __repr__(self):
    #     return
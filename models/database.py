import os
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

engine = create_engine(os.environ.get('sqlite'))
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    from models.author import Author
    from models.book import Books
    Base.metadata.create_all(bind=engine)


# QUERIES
from models.author import Author
from models.book import Books


def save(obj: object) -> bool:
    """
           :PARAMS: Obj: Object
           :RETURNS: bool: rue if successful, False otherwise.
           """
    try:
        db_session.add(obj)
        db_session.commit()
    except IntegrityError:
        return False

    return True


def find_author(email: str) -> object:
    """
       PARAMS str: email
       :RETURNS: object if found, None if no result.
       """
    try:
        result = db_session.query(Author).filter(Author.email == email).first()
        return result
    except NoResultFound:
        return None


def find_book_title(title: str) -> object:
    """
       PARAMS str: title
       :RETURNS: object if found, None if no result.
       """
    try:
        result = db_session.query(Books).filter(Books.title == title).first()
        return result
    except NoResultFound:
        return None


def all_books() -> object:
    try:
        return Books.query.all()
    except NoResultFound:
        return None


def edit_book(**kwargs) -> bool:
    """
       :param kwargs: title, new_title, new_description, new_genre
       :return: bool: True if successful, False otherwise.
       """
    data = {}
    for key, value in kwargs.items():
        data[key] = value

    try:

        result = db_session.query(Books).filter(Books.title == data['title']).first()
    except NoResultFound:
        return None

    if 'new_title' in data:
        result.title = data['new_title']

    if 'new_description' in data:
        result.description = data['new_description']

    if 'new_genre' in data:
        result.genre = data['new_genre']

    db_session.commit()
    return True


def edit_author(**kwargs) -> bool:
    """
    :param kwargs: email, new_name, new_about
    :return: bool: True if successful, False otherwise.
    """

    data = {}
    for key, value in kwargs.items():
        data[key] = value

    try:
        result = db_session.query(Author).filter(Author.email == data['email']).first()
    except NoResultFound:
        return None

    if data['new_name']:
        result.name = data['new_name']

    if data['new_about']:
        result.about = data['new_about']

    db_session.commit()
    return True


def del_book(title: str) -> bool:
    """
    :PARAMS: title
    :RETURNS: bool: True if successful, False otherwise.
    """
    user = db_session.query(Books).filter(Books.title == title).first()
    db_session.delete(user)
    db_session.commit()
    return True

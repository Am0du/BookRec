import os
from models.database import (db_session, init_db,
                             save, del_book, edit_book, edit_author, find_author, find_book_title, all_books)
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, jsonify, url_for
from models.author import Author
from models.book import Books
import jwt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('s_key')
# app.config['SQLALCHEMY_DATA_URI'] = os.environ.get('sqlite')
init_db()


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"info": 'No Authorization token attached', "isSuccessful": "false"}), 400
        try:
            jwt.decode(token, app.secret_key, algorithms=['HS256'])
        except jwt.DecodeError:
            return jsonify(info='Invalid Token', isSuccessful='false', status_code=403), 403
        except jwt.ExpiredSignatureError:
            return jsonify(info='Expired Token', isSuccessful='false', status_code=403), 403
        return func(*args, **kwargs)

    return decorated


def header_detail():
    token = request.headers.get('Authorization')
    token_data = jwt.decode(token, app.secret_key, algorithms=['HS256'])

    return token_data.get('email')

#ROUTES
@app.route('/api/register', methods=['POST'])
def register():
    """
    Register Author

    This function registers a new author by extracting data from a JSON request.

    Parameters:
        None (uses data from the request)

    Returns:
        A JSON response indicating the success or failure of the registration process.
    """
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    about = data.get('about')

    if name and password and email:
        new_pass = generate_password_hash(password=password, salt_length=18)
        obj = Author(name=name, email=email, password=new_pass, about=about)
        response = save(obj)
        if response:
            return jsonify(isSuccessful='true', redirectUri=url_for('login'), info='User created'), 201
        else:
            return jsonify(isSuccessful='false', info='User already exist', status_code=409), 409
    else:
        return jsonify(isSuccessful='false', info='User data not complete'), 400


@app.route('/api/login', methods=['POST'])
def login():
    """
        Login Author

        This function handles the login process for an author by extracting email and password
        from the JSON data obtained from the request.

        Parameters:
            None (uses data from the request)

        Returns:
            A JSON response indicating the success or failure of the login process.
        """

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    result = find_author(email)
    if result:
        if check_password_hash(result.password, password):
            token = jwt.encode({
                'email': result.email,
                'exp': datetime.utcnow() + timedelta(hours=7)
            },
                app.secret_key, algorithm='HS256')
            return jsonify(isSuccessful='true', header_token=token, info='token expires in 7 hours', status_code=200), 200
        else:
            return jsonify(isSuccessful='false', info='Invalid user login details', status_code=400), 400
    else:
        return jsonify(isSuccessful='false', info='Invalid user login details', status_code=400), 400


@app.route('/api/add_book', methods=['POST'])
@token_required
def add_book():
    """
    Add book to an Author

    This function allows an author to add a new book by extracting necessary data from the request JSON.

    Parameters:
        None (uses data from the request and header)

    Returns:
        A JSON response indicating the success or failure of the book addition process.
    """

    email = header_detail()
    author = find_author(email)

    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    genre = data.get('genre')
    if title and description and genre:
        book = Books(title=title, description=description, genre=genre, author=author.id)
        saved = save(book)
        if saved:
            response = {
                'isSuccessful': 'true',
                'info': 'Book created and stored successfully',
                'data':
                    {'title': title,
                     'description': description,
                     'genre': genre},
                'status_code': 201
            }

            return jsonify(response), 201
        else:
            return jsonify(isSuccessful='false', info='Book title already exist', status_code=400), 400

    return jsonify(isSuccessful='false', info='Book details are not complete', status_code=400), 400


@app.route('/api/edit_book', methods=['PUT'])
@token_required
def edit_author_book():
    """
        Author edits his books

        This function allows an author to edit their books by providing new information.

        Parameters:
            None (uses data from the request and header)

        Returns:
            A JSON response indicating the success or failure of the book editing process.
    """

    data = request.get_json()
    title = data.get('title')
    new_title = data.get('new_title')
    new_genre = data.get('new_genre')
    new_description = data.get('new_description')

    author_email = header_detail()
    author = find_author(author_email)
    author_books = author.books
    for book in author_books:
        if book.title == title:
            old_book = {'title': book.title,
                        'genre': book.genre,
                        'description': book.description
                        }
            edited = edit_book(title=title, new_title=new_title, new_description=new_description, new_genre=new_genre)

            if new_title:
                new_book = find_book_title(new_title)
            else:
                new_book = find_book_title(title)
            if edited:
                result = {
                    'isSuccessful': 'true',
                    'info': 'Book details updated',
                    'status_code': 200,
                    'data': {
                        'old_data': old_book,
                        'new_data': {
                            'title': new_book.title,
                            'genre': new_book.genre,
                            'description': new_book.description
                        }
                    },
                }

                return jsonify(result), 200

    if find_book_title(title):
        return jsonify(isSuccessful='false', info=f'Not authorized to delete {title}', status_code=401), 401
    else:
        return jsonify(isSuccessful='false', info='Book does not exist', status_code=404), 404


# @app.route('/api/change', methods=['PUT'])
# def change():
#     """ Author changes his password """
#     ...

@app.route('/api/edit_author', methods=['PUT'])
@token_required
def edit_detail():
    """
        Author edits his details

        This function allows an author to edit their details such as name and about section.

        Parameters:
            None (uses data from the request and header)

        Returns:
            A JSON response indicating the success or failure of the author details editing process.
        """

    author_email = header_detail()
    data = request.get_json()
    name = data.get('name')
    about = data.get('about')
    author = find_author(author_email)
    old_author ={
        'name': author.name,
        'about': author.about
    }
    if name or about:
        changed = edit_author(email=author_email, new_name=name, new_about=about)
        if changed:
            new_author = find_author(author_email)
            result = {
                'isSuccessful': 'true',
                'info': 'Author details updated',
                'status_code': 200,
                'data': {
                    'old_data': old_author,
                    'new_data': {
                        'name': new_author.name,
                        'about': new_author.about,
                    }
                },
            }
            return jsonify(result), 200
    else:
        return jsonify(isSuccessful='false', info='Invalid request body', status_code=400), 400


@app.route('/api/delete_book', methods=['DELETE'])
@token_required
def delete():
    """
       Author deletes his books

       This function allows an author to delete their books by providing the title of the book.

       Parameters:
           None (uses data from the request and header)

       Returns:
           A JSON response indicating the success or failure of the book deletion process.
    """

    author_email = header_detail()
    data = request.get_json()
    title = data.get('title')
    author = find_author(author_email)
    author_books = author.books

    for book in author_books:
        if book.title == title:
            del_book(title)

            return jsonify(isSuccessful='true', info=f'Book({title}) has been deleted', status_code=200), 200

    if find_book_title(title):
        return jsonify(isSuccessful='false', info=f'Not authorized to delete {title}', status_code=401), 401
    else:
        return jsonify(isSuccessful='false', info='Book does not exist', status_code=404), 404


@app.route('/api/genre/<genre>', methods=['GET'])
def find_genre(genre):
    """
    Returns books with requested genre

    This function retrieves books with the specified genre.

    Parameters:
        genre (str): The genre of the books to retrieve

    Returns:
        A JSON response containing books with the requested genre, or a message indicating the genre was not found.
    """
    book_list = all_books()
    genre_list = []
    for book in book_list:
        if book.genre == genre:
            book_dict = {
                'title': book.title,
                'genre': book.genre,
                'description': book.description,
                'author': book.author.name,
                'about author': book.author.about
            }
            genre_list.append(book_dict)

    if genre_list:
        return jsonify(isSuccessful='true', info=f'genre found', books=genre_list, status_code=200), 200

    return jsonify(isSuccessful='false', info=f'{genre} genre not found', status_code=404), 404


@app.route('/api/book', methods=['GET'])
def book():
    """
       Returns books with the same title

       This function retrieves details of a book with the specified title.

       Parameters:
           None (uses data from the request)

       Returns:
           A JSON response containing details of the book with the requested title, or a message indicating the book was not found.
       """

    data = request.get_json()
    title = data.get('title')
    result = find_book_title(title)
    if result:
        data = {
            'isSuccessful': 'false',
            'info': 'resource found',
            'status_code': 200,
            'data': {
                'title': result.title,
                'description': result.description,
                'genre': result.genre,
                'author': result.author.name,
                'about_author': result.author.about
            }
        }
        return jsonify(data), 200
    return jsonify(isSuccessful='false', info='Book does not exist', status_code=404), 404


@app.route('/api/books', methods=['GET'])
def books():
    """
        Returns all books

        This function retrieves details of all available books.

        Parameters:
            None

        Returns:
            A JSON response containing details of all available books.
    """
    book_list = all_books()
    # book_lis = [lis.title for lis in book_list]
    # print(book_lis)

    data_list = []
    for i in book_list:
        data_dict = {}
        data_dict['title'] = i.title
        data_dict['description'] = i.description
        data_dict['genre'] = i.genre
        data_dict['author'] = i.author.name
        data_dict['about_author'] = i.author.about

        data_list.append(data_dict)

    return jsonify(isSuccessful='true', books=data_list, status_code=200), 200

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    app.run(debug=True)

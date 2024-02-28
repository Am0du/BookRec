# API Documentation

## Register
Register Author.

- **URL**: `/api/register`
- **Method**: `POST`
- **Request Body**: 
    ```json
    {
        "name": "string",
        "email": "string",
        "password": "string",
        "about": "string"
    }
    ```
- **Response**: 
    - Success:
        - Status Code: `201`
        - Body:
            ```json
            {
                "isSuccessful": "true",
                "redirectUri": "string",
                "info": "User created",
                "status_code": 201
            }
            ```
    - Failure:
        - Status Code: `400` or `409`
        - Body:
            ```json
            {
                "isSuccessful": "false",
                "info": "User data not complete" (or "User already exists"),
                "status_code": 400 (or 409)
            }
            ```

## Login
Login Author.

- **URL**: `/api/login`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
        "email": "string",
        "password": "string"
    }
    ```
- **Response**: 
    - Success:
        - Status Code: `200`
        - Body:
            ```json
            {
                "isSuccessful": "true",
                "header_token": "string",
                "info": "token expires in 7 hours",
                "status_code": 200
            }
            ```
    - Failure:
        - Status Code: `400`
        - Body:
            ```json
            {
                "isSuccessful": "false",
                "info": "Invalid user login details",
                "status_code": 400
            }
            ```

## Add Book
Add book to an Author.

- **URL**: `/api/add_book`
- **Method**: `POST`
- **Request Headers**:
    - Authorization: `Bearer <JWT>`
- **Request Body**:
    ```json
    {
        "title": "string",
        "description": "string",
        "genre": "string"
    }
    ```
- **Response**: 
    - Success:
        - Status Code: `201`
        - Body:
            ```json
            {
                "isSuccessful": "true",
                "info": "Book created and stored successfully",
                "data": {
                    "title": "string",
                    "description": "string",
                    "genre": "string"
                },
                "status_code": 201
            }
            ```
    - Failure:
        - Status Code: `400`
        - Body:
            ```json
            {
                "isSuccessful": "false",
                "info": "Book details are not complete",
                "status_code": 400
            }
            ```

## Edit Book
Author edits his books.

- **URL**: `/api/edit_book`
- **Method**: `PUT`
- **Request Headers**:
    - Authorization: `Bearer <JWT>`
- **Request Body**:
    ```json
    {
        "title": "string",
        "new_title": "string",
        "new_description": "string",
        "new_genre": "string"
    }
    ```
- **Response**: 
    - Success:
        - Status Code: `200`
        - Body:
            ```json
            {
                "isSuccessful": "true",
                "info": "Book details updated",
                "status_code": 200,
                "data": {
                    "old_data": {
                        "title": "string",
                        "genre": "string",
                        "description": "string"
                    },
                    "new_data": {
                        "title": "string",
                        "genre": "string",
                        "description": "string"
                    }
                }
            }
            ```
    - Failure:
        - Status Code: `404` or `401`
        - Body:
            ```json
            {
                "isSuccessful": "false",
                "info": "Book does not exist" (or "Not authorized to delete" or "Book does not exist or Unauthorized"),
                "status_code": 404 (or 401)
            }
            ```

## Edit Author
Author edits his details.

- **URL**: `/api/edit_author`
- **Method**: `PUT`
- **Request Headers**:
    - Authorization: `Bearer <JWT>`
- **Request Body**:
    ```json
    {
        "name": "string",
        "about": "string"
    }
    ```
- **Response**: 
    - Success:
        - Status Code: `200`
        - Body:
            ```json
            {
                "isSuccessful": "true",
                "info": "Author details updated",
                "status_code": 200,
                "data": {
                    "old_data": {
                        "name": "string",
                        "about": "string"
                    },
                    "new_data": {
                        "name": "string",
                        "about": "string"
                    }
                }
            }
            ```
    - Failure:
        - Status Code: `400`
        - Body:
            ```json
            {
                "isSuccessful": "false",
                "info": "Invalid request body",
                "status_code": 400
            }
            ```


## Delete Book
Author deletes his books.

- **URL**: `/api/delete_book`
- **Method**: `DELETE`
- **Request Headers**:
    - Authorization: `Bearer <JWT>`
- **Request Body**:
    ```json
    {
        "title": "string"
    }
    ```
- **Response**: 
    - Success:
        - Status Code: `200`
        - Body:
            ```json
            {
                "isSuccessful": "true",
                "info": "Book(string) has been deleted",
                "status_code": 200
            }
            ```
    - Failure:
        - Status Code: `404` or `401`
        - Body:
            ```json
            {
                "isSuccessful": "false",
                "info": "Book does not exist" (or "Not authorized to delete" or "Book does not exist"),
                "status_code": 404 (or 401)
            }
            ```
## Author's Books
Returns all books by author.

- **URL**: `/api/my_books`
- **Method**: `GET`
- **Request Headers**:
    - Authorization: `Bearer <JWT>`
- **Response**: 
    - Success:
        - Status Code: `200`
        - Body: A list of dictionaries containing book details.
            ```json
            [
                {
                    "title": "string",
                    "description": "string",
                    "genre": "string",
                    "author": "string"
                }
            ]
            ```
    - Failure:
        - Status Code: `404`
        - Body:
            ```json
            {
                "isSuccessful": "false",
                "info": "No book found",
                "status_code": 404
            }
            ```
          

## Get Books by Genre
Returns books with requested genre.

- **URL**: `/api/genre/<genre>`
- **Method**: `GET`
- **Response**: 
    - Success:
        - Status Code: `200`
        - Body:
            ```json
            {
                "isSuccessful": "true",
                "info": "genre found",
                "books": [
                    {
                        "title": "string",
                        "genre": "string",
                        "description": "string"
                    }
                ],
                "status_code": 200
            }
            ```
    - Failure:
        - Status Code: `404`
        - Body:
            ```json
            {
                "isSuccessful": "false",
                "info": "<genre> genre not found",
                "status_code": 404
            }
            ```

## Get Book by Title
Returns books with the same title.

- **URL**: `/api/book`
- **Method**: `GET`
- **Request Body**:
    ```json
    {
        "title": "string"
    }
    ```
- **Response**: 
    - Success:
        - Status Code: `200`
        - Body:
            ```json
            {
                "isSuccessful": "false",
                "info": "resource found",
                "status_code": 200,
                "data": {
                    "title": "string",
                    "description": "string",
                    "genre": "string",
                    "author": "string"
                }
            }
            ```
    - Failure:
        - Status Code: `404`
        - Body:
            ```json
            {
                "isSuccessful": "false",
                "info": "Book does not exist",
                "status_code": 404
            }
            ```

## Get All Books
Returns all books.

- **URL**: `/api/books`
- **Method**: `GET`
- **Response**: 
    - Success:
        - Status Code: `200`
        - Body: A list of dictionaries containing book details.
            ```json
            [
                {
                    "title": "string",
                    "description": "string",
                    "genre": "string",
                    "author": "string"
                }
            ]
            ```

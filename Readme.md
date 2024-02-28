# BookRec Backend Service API Documentation

A backend service for managing user registration, authentication, and book management for authors. Here's a summary of what each endpoint does:

## Register

Allows users to register as authors by providing their name, email, password, and optional about information. Upon successful registration, a user is created, and they receive a success message along with a redirect URL for login.

## Login

Allows registered users to log in by providing their email and password. Upon successful authentication, a JWT (JSON Web Token) is generated and returned, which can be used for subsequent authorized requests.

## Add Book

Allows authenticated authors to add books to their collection. Authors must provide the title, description, and genre of the book. Upon successful addition, the book details are stored, and a success message is returned.

## Edit Book

Allows authenticated authors to edit the details of their books. Authors can update the title, description, and genre of an existing book. Upon successful edit, the updated book details are returned along with a success message.

## Edit Author

Allows authenticated authors to edit their own details, such as name and about information. Upon successful edit, the updated author details are returned along with a success message.

## Delete Book

Allows authenticated authors to delete their own books. Authors must provide the title of the book to be deleted. Upon successful deletion, a success message is returned.

## My Books

This route is responsible for retrieving the books authored by the authorized author.

## Get Books by Genre

Allows users to retrieve a list of books based on a specific genre. Users provide the genre as a parameter in the URL. Upon successful retrieval, a list of books matching the genre is returned.

## Get Book by Title

Allows users to retrieve details of a book based on its title. Users provide the title of the book in the request body. Upon successful retrieval, details of the book are returned.

## Get All Books

Allows users to retrieve details of all books stored in the system. Upon successful retrieval, a list of all books with their details is returned.

Overall, this API provides functionality for user authentication, book management, and retrieval of book information, catering specifically to authors.

##  [API Documentation](Documentation.md)
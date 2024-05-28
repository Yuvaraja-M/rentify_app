# rentify_app
Api based creation for managing rents Presidio project

# Rentify App

Rentify is a web application designed to manage rental properties, allowing users to register, log in, and manage property listings. Built with FastAPI, the app provides a robust API with comprehensive documentation available via Swagger. The backend utilizes SQLite for data storage.

## Features

- User registration and authentication
- Property creation, updating, and deletion
- Property filtering based on various criteria
- API documentation with Swagger

## Project Files

### `crud.py`

Contains the CRUD operations for users and properties. Handles password hashing and verification, user creation, property creation, and property filtering.

### `database.py`

Sets up the SQLite database connection using SQLAlchemy and defines the `SessionLocal` for database interactions.

### `main.py`

Defines the FastAPI application, including routes for user registration, login, and property management. Also includes token generation and user authentication.

### `models.py`

Defines the SQLAlchemy models for `User` and `Property`.

### `schemas.py`

Defines the Pydantic schemas for request and response models, ensuring data validation.

### `run.py`

Entry point for running the application using Uvicorn.

## Requirements

- Python 3.8+
- FastAPI
- SQLAlchemy
- Uvicorn
- Passlib
- Python-Jose

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/Yuvaraja-M/rentify.git
   cd rentify
2. create and activate a virtual environment:
   ```
     python -m venv venv
     source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. Install dependencies
   ```
   pip install -r requirements.txt

4. Run the application
    ```
    python run.py
5. Access the API documentation:
Open your browser and navigate to http://127.0.0.1:8080/docs.

## Deployment
The project is deployed at https://rentify-app-lm13.onrender.com/docs

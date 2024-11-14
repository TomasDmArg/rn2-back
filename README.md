# Todo API

A simple Todo API with user authentication built using FastAPI and SQLAlchemy.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/TomasDmArg/rn1-back/
   cd rn1-back
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `.env` file in the root directory of the project.
2. Add the following environment variables to the `.env` file:
   ```
   DB_HOST=your_database_host
   DB_NAME=your_database_name
   DB_USER=your_database_user
   DB_PASSWORD=your_database_password
   SECRET_KEY=your_secret_key_for_jwt
   ```

## Database Setup

1. Connect to your MySQL server.
2. Create a new database:
   ```sql
   CREATE DATABASE your_database_name;
   ```
3. Use the provided SQL script to create the necessary tables:
   ```
   mysql -u your_username -p your_database_name < /app/utils/create_tables.sql
   ```

## Running the Application

1. Ensure your virtual environment is activated.
2. Start the FastAPI server:
   ```
   uvicorn app.main:app --reload
   ```
3. The API will be available at `http://localhost:8000`

## API Documentation

- Swagger UI (interactive documentation): `http://localhost:8000/docs`
- ReDoc (alternative documentation): `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

## Project Structure

```
todo-api/
├── app/
│   ├── auth/
│   │   └── jwt_handler.py
│   ├── crud/
│   │   ├── todo.py
│   │   └── user.py
│   ├── models/
│   │   ├── todo.py
│   │   └── user.py
│   ├── routes/
│   │   ├── todo.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── todo.py
│   │   └── user.py
│   ├── utils/
│   │   └── create_tables.sql
│   ├── database.py
│   └── main.py
├── requirements.txt
└── README.md
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
# rn02back-tomi

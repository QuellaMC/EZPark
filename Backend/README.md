# EZPark Backend

EZPark Backend is a scalable and modular backend solution for the EZPark website. Built with FastAPI, it is designed to be easily extendable, allowing each API endpoint to reside in its own Python file. Additionally, it includes a `utils` folder for utility modules such as database connections, authentication, and more.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Extending the Backend](#extending-the-backend)
- [Contributing](#contributing)

## Features

- **Modular Design**: Each API endpoint is organized in separate Python files for better maintainability and scalability.
- **Utility Modules**: Common functionalities like database connections and authentication are centralized in the `utils` folder.
- **Database Integration**: Supports SQLAlchemy for ORM with MySQL as the database backend.
- **Automatic Documentation**: FastAPI provides interactive API documentation with Swagger UI and ReDoc.
- **Testing**: Includes a testing framework with pytest to ensure reliability and correctness.
- **Environment Configuration**: Manage configurations through environment variables using Pydantic's `BaseSettings`.

## Project Structure

```
ezpark_backend/
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── endpoint1.py
│   │   ├── endpoint2.py
│   │   └── ... (additional endpoint files)
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── auth.py
│   │   └── ... (additional utility modules)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── ... (additional model files)
│   └── config/
│       ├── __init__.py
│       └── settings.py
├── tests/
│   ├── __init__.py
│   ├── test_endpoint1.py
│   └── ... (additional test files)
├── requirements.txt
├── README.md
└── .env
```

### Detailed Structure

- **`app/main.py`**: The entry point of the FastAPI application. It initializes the app and includes all API routes.
- **`app/api/`**: Contains individual API endpoint files, each defining its own routes and logic.
- **`app/utils/`**: Houses utility modules such as database connections, authentication mechanisms, etc.
- **`app/models/`**: Defines the database models using SQLAlchemy.
- **`app/config/`**: Manages configuration settings, including environment variables.
- **`tests/`**: Contains test cases for the API endpoints to ensure they function correctly.
- **`requirements.txt`**: Lists all project dependencies.
- **`.env`**: Stores environment-specific configurations and sensitive information (should not be committed to version control).

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- MySQL Server

### Steps

1. **Clone the Repository**
2. **Create a Virtual Environment**
   
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install Dependencies**
   
   ```bash
   pip install -r requirements.txt
   ```
4. **Install MySQL Server**
   
   - **Windows**: Download and install MySQL from [MySQL Downloads](https://dev.mysql.com/downloads/mysql/).
   - **macOS**: Use Homebrew:
     
     ```bash
     brew install mysql
     ```
   - **Linux**: Use your distribution's package manager, e.g., for Ubuntu:
     
     ```bash
     sudo apt update
     sudo apt install mysql-server
     ```
5. **Start MySQL Server**
   
   - **Windows**: Start the MySQL service from the Services panel.
   - **macOS/Linux**:
     
     ```bash
     sudo service mysql start
     ```
6. **Secure MySQL Installation (Optional but Recommended)**
   
   ```bash
   sudo mysql_secure_installation
   ```

## Configuration

1. **Create a MySQL Database and User**
   
   Log into the MySQL shell:
   
   ```bash
   mysql -u root -p
   ```
   
   Then execute the following commands:
   
   ```sql
   CREATE DATABASE ezpark_db;
   CREATE USER 'ezpark_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON ezpark_db.* TO 'ezpark_user'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   ```
2. **Environment Variables**
   
   Create a `.env` file in the root directory and add the following configurations:
   
   ```env
   DATABASE_URL=mysql+pymysql://ezpark_user:your_password@localhost/ezpark_db
   SECRET_KEY=your-secret-key
   ```
   
   - **`DATABASE_URL`**: Specifies the MySQL database connection string.
   - **`SECRET_KEY`**: A secret key used for security purposes, such as JWT token generation.
3. **Settings Management**
   
   The `app/config/settings.py` file uses Pydantic's `BaseSettings` to manage configurations. It automatically reads from the `.env` file.
   
   ```python
   # app/config/settings.py
   from pydantic import BaseSettings
   
   class Settings(BaseSettings):
       database_url: str = "mysql+pymysql://ezpark_user:your_password@localhost/ezpark_db"
       secret_key: str = "your-secret-key"
   
       class Config:
           env_file = ".env"
   
   settings = Settings()
   ```
4. **Update `database.py` for MySQL**
   
   Ensure that the database utility is configured to use MySQL.
   
   ```python
   # app/utils/database.py
   from sqlalchemy import create_engine
   from sqlalchemy.orm import sessionmaker, declarative_base
   from app.config.settings import settings
   
   engine = create_engine(
       settings.database_url,
       pool_pre_ping=True
   )
   SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   Base = declarative_base()
   
   def get_db():
       db = SessionLocal()
       try:
           yield db
       finally:
           db.close()
   ```

## Running the Application

Use Uvicorn to run the FastAPI application.

```bash
uvicorn app.main:app --reload
```

- The `--reload` flag enables auto-reloading of the server upon code changes.
- By default, the application will be accessible at `http://127.0.0.1:8000`.

### Accessing API Documentation

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Testing

The project uses `pytest` for testing. Tests are located in the `tests/` directory.

1. **Install Test Dependencies**
   
   Ensure that `pytest` is installed. It should already be included in `requirements.txt`. If not, install it:
   
   ```bash
   pip install pytest
   ```
2. **Run Tests**
   
   ```bash
   pytest
   ```
   
   This command will discover and run all test cases in the `tests/` directory.

### Example Test Case

```python
# tests/test_endpoint1.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_endpoint1():
    response = client.get("/api/endpoint1/")
    assert response.status_code == 200
    assert response.json() == {"message": "Endpoint1 data"}
```

## Extending the Backend

### Adding a New API Endpoint

1. **Create a New Endpoint File**
   
   Create a new Python file in the `app/api/` directory, e.g., `new_endpoint.py`.
   
   ```python
   # app/api/new_endpoint.py
   from fastapi import APIRouter, Depends
   from app.utils.database import get_db
   from sqlalchemy.orm import Session
   
   router = APIRouter()
   
   @router.get("/")
   async def read_new_endpoint(db: Session = Depends(get_db)):
       # Your logic here
       return {"message": "New endpoint data"}
   ```
2. **Include the New Router in `main.py`**
   
   ```python
   # app/main.py
   from fastapi import FastAPI
   from app.api import endpoint1, endpoint2, new_endpoint  # Import the new endpoint
   
   app = FastAPI(
       title="EZPark Backend",
       description="Backend API for EZPark website",
       version="1.0.0"
   )
   
   app.include_router(endpoint1.router, prefix="/api/endpoint1", tags=["Endpoint1"])
   app.include_router(endpoint2.router, prefix="/api/endpoint2", tags=["Endpoint2"])
   app.include_router(new_endpoint.router, prefix="/api/new_endpoint", tags=["NewEndpoint"])  # Include the new router
   ```
3. **Create Models and Utilities as Needed**
   
   If your new endpoint requires new database models or utility functions, add them to the respective directories (`app/models/` or `app/utils/`).
4. **Write Tests**
   
   Add a new test file in the `tests/` directory, e.g., `test_new_endpoint.py`, and write test cases for your new endpoint.
   
   ```python
   # tests/test_new_endpoint.py
   from fastapi.testclient import TestClient
   from app.main import app
   
   client = TestClient(app)
   
   def test_read_new_endpoint():
       response = client.get("/api/new_endpoint/")
       assert response.status_code == 200
       assert response.json() == {"message": "New endpoint data"}
   ```

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. **Fork the Repository**
2. **Create a New Branch**
   
   ```bash
   git checkout -b feature/YourFeature
   ```
3. **Make Your Changes**
4. **Commit Your Changes**
   
   ```bash
   git commit -m "Add Your Feature"
   ```
5. **Push to Your Fork**
   
   ```bash
   git push origin feature/YourFeature
   ```
6. **Create a Pull Request**


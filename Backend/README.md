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
- [License](#license)
- [Contact](#contact)

## Features

- **Modular Design**: Each API endpoint is organized in separate Python files for better maintainability and scalability.
- **Utility Modules**: Common functionalities like database connections and authentication are centralized in the `utils` folder.
- **Database Integration**: Supports SQLAlchemy for ORM with a configurable database backend.
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

### Steps

1. **Clone the Repository**
   
   ```bash
   git clone https://github.com/yourusername/ezpark_backend.git
   cd ezpark_backend
   ```
2. **Create a Virtual Environment**
   
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install Dependencies**
   
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Environment Variables**
   
   Create a `.env` file in the root directory and add the following configurations:
   
   ```env
   DATABASE_URL=sqlite:///./ezpark.db
   SECRET_KEY=your-secret-key
   ```
   
   - **`DATABASE_URL`**: Specifies the database connection string. The example uses SQLite, but you can switch to other databases like PostgreSQL by updating this URL.
   - **`SECRET_KEY`**: A secret key used for security purposes, such as JWT token generation.
2. **Settings Management**
   
   The `app/config/settings.py` file uses Pydantic's `BaseSettings` to manage configurations. It automatically reads from the `.env` file.
   
   ```python
   # app/config/settings.py
   from pydantic import BaseSettings
   
   class Settings(BaseSettings):
       database_url: str = "sqlite:///./ezpark.db"
       secret_key: str = "your-secret-key"
   
       class Config:
           env_file = ".env"
   
   settings = Settings()
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




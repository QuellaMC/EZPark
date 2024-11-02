# EZPark Windows Client Directory Structure

## Overview

The EZPark Windows client application provides users with an interface to access the EZPark platform, allowing for parking space search, booking, and management through a Windows environment. The client interacts with the backend API for user authentication and real-time data operations. Below is the detailed directory structure of the client application.

## Directory Structure

```
ezpark_windows_client/
├── main.py
├── src/
│   ├── ui/
│   │   ├── login_ui.py
│   │   ├── register_ui.py
│   │   └── dashboard_ui.py
│   ├── controllers/
│   │   ├── auth_controller.py
│   │   └── parking_controller.py
│   ├── models/
│   │   ├── user.py
│   │   └── parking_space.py
│   └── utils/
│       ├── api_client.py
│       └── config.py
├── assets/
│   ├── images/
│   └── styles/
└── README.md
```

### 1. `main.py`

- **Description**: The entry point for the application. Initializes the main window and loads the login interface. This script ties together different components of the application to provide a cohesive user experience.

### 2. `src/`

- **Description**: Contains the main source code for the application, organized into subdirectories for UI, controllers, models, and utility functions.

#### 2.1 `ui/`

- **`login_ui.py`**: Manages the login user interface, allowing users to enter their credentials and authenticate.
- **`register_ui.py`**: Manages the registration user interface, allowing new users to create an account.
- **`dashboard_ui.py`**: Provides the main application dashboard after successful login, displaying parking-related features and information.

#### 2.2 `controllers/`

- **`auth_controller.py`**: Handles authentication logic, including login, registration, and token management.
- **`parking_controller.py`**: Manages interactions with parking-related data, such as listing available parking spaces and updating parking statuses.

#### 2.3 `models/`

- **`user.py`**: Defines the user data model, including attributes like email, name, and authentication status.
- **`parking_space.py`**: Defines the parking space data model, including attributes like address, availability, and permit requirements.

#### 2.4 `utils/`

- **`api_client.py`**: Provides a wrapper around the backend API, simplifying the process of making HTTP requests and handling responses.
- **`config.py`**: Stores configuration data such as API URLs and settings for easy adjustment and maintenance.

### 3. `assets/`

- **Description**: Contains static assets used by the application, such as images and style files.

#### 3.1 `images/`

- **Purpose**: Stores image assets such as logos, icons, and background images used in the UI.

#### 3.2 `styles/`

- **Purpose**: Contains styling files (e.g., CSS or theme settings) to ensure a consistent visual appearance across the application.

### 4. `README.md`

- **Description**: Provides an overview of the application, instructions for installation, setup, and usage. It serves as the primary documentation for developers and users.

1. **Register and Log In**: Users can create an account or log in using their credentials. Authentication is managed through the backend API, ensuring secure access.

   - **Note**: Users can view parking space availability without logging in. Logging in is required for submitting parking data and accessing administrator features. Authentication is managed through the backend API, ensuring secure access.

2. **Parking Dashboard**: After logging in, users can view available parking spaces, check their status, and interact with the parking system. This feature is built with user-friendly UI components to provide real-time parking availability and booking options.

3. **API Integration**: The client makes use of the backend API for authentication (`auth/` endpoints) and parking operations (`parking_spaces/` endpoints). The `api_client.py` utility is responsible for handling all API requests and responses, ensuring smooth communication with the backend.

4. **Extensibility**: The modular structure of the application allows for easy future extensions, such as adding new features (e.g., payment integration, notifications) by adding new controllers, models, and UI components.

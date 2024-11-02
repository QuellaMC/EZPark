# EZPark Backend API Specification

## Table of Contents

1. [API Directory Structure](#1-api-directory-structure)
2. [Authentication APIs (`auth/`)](#2-authentication-apis-auth)
   - [2.1.1 Register (`register.py`)](#211-register-registerpy)
   - [2.1.2 Login (`login.py`)](#212-login-loginpy)
   - [2.1.3 Email Verification (`email_verification.py`)](#213-email-verification-email_verificationpy)
   - [2.1.4 Resend Verification Email (`resend_verification.py`)](#214-resend-verification-email-resend_verificationpy)
   - [2.1.5 Get Verification Code (`get_verification_code.py`)](#215-get-verification-code-get_verification_codepy)
   - [2.1.6 Verify Verification Code (`verify_verification_code.py`)](#216-verify-verification-code-verify_verification_codepy)
3. [Admin APIs (`admin/`)](#3-admin-apis-admin)
   - [3.1.1 User Management (`user_management.py`)](#311-user-management-user_managementpy)
   - [3.1.2 Parking Submission Management (`parking_submission_management.py`)](#312-parking-submission-management-parking_submission_managementpy)
   - [3.1.3 Configuration Management (`config_management.py`)](#313-configuration-management-config_managementpy)
4. [Parking Spaces APIs (`parking_spaces/`)](#4-parking-spaces-parking_spaces)
   - [4.1.1 Create Parking Space (`create_parking_space.py`)](#411-create-parking-space-create_parking_spacepy)
   - [4.1.2 Set Full Status (`set_full_status.py`)](#412-set-full-status-set_full_statuspy)
   - [4.1.3 List Parking Spaces (`list_parking_spaces.py`)](#413-list-parking-spaces-list_parking_spacespy)
   - [4.1.4 Get Parking Space Details (`get_parking_space_details.py`)](#414-get-parking-space-details-get_parking_space_detailspy)
5. [Submissions APIs (`submissions/`)](#5-submissions-apis-submissions)
   - [5.1.1 Submit Parking Space (`submit_parking_space.py`)](#511-submit-parking-space-submit_parking_spacepy)
6. [Utils APIs (`utils/`)](#6-utils-apis-utils)
   - [6.1 Initialize Package (`__init__.py`)](#61-initialize-package-initpy)
   - [6.2 Additional Utility Modules](#62-additional-utility-modules)

---

## 1. API Directory Structure

The following directory structure organizes the API endpoints into logical modules, ensuring maintainability and scalability.

```
ezpark_backend/
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth/
│   │   │   ├── __init__.py
│   │   │   ├── register.py
│   │   │   ├── login.py
│   │   │   ├── email_verification.py
│   │   │   └── resend_verification.py
│   │   ├── admin/
│   │   │   ├── __init__.py
│   │   │   ├── user_management.py
│   │   │   ├── parking_submission_management.py
│   │   │   └── config_management.py
│   │   ├── parking_spaces/
│   │   │   ├── __init__.py
│   │   │   ├── create_parking_space.py
│   │   │   ├── set_full_status.py
│   │   │   ├── list_parking_spaces.py
│   │   │   └── get_parking_space_details.py
│   │   ├── submissions/
│   │   │   ├── __init__.py
│   │   │   └── submit_parking_space.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── logger.py
│   │       ├── permissions.py
│   │       └── rate_limiter.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── auth.py
│   │   ├── email.py
│   │   └── logger.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── parking_space.py
│   │   └── parking_submission.py
│   └── config/
│       ├── __init__.py
│       └── settings.py
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_admin.py
│   ├── test_parking_spaces.py
│   └── test_submissions.py
├── requirements.txt
├── README.md
└── .env
```

## 2. Authentication APIs (`auth/`)

Handles user registration, login, email verification, and resending verification emails with enhanced security via Google reCAPTCHA.

### 2.1.1 Register (`register.py`)

- **Path**: `/api/auth/register`
- **Method**: `POST`
- **Description**: Registers a new user account, validates Google reCAPTCHA, and sends a verification email.
- **Authentication**: No prior authentication required.

#### Request

- **Headers**:
  
  - `Content-Type: application/json`
- **Body**:
  
  ```json
  {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "password": "SecurePassword123!",
    "recaptcha_token": "03AGdBq25..."
  }
  ```

#### Response

- **Status Code**: `201 Created`
- **Body**:
  
  ```json
  {
    "message": "Account created successfully. Please check your email to verify your account."
  }
  ```
- **Error Responses**:
  
  - `400 Bad Request`:
    
    ```json
    {
      "detail": "Invalid input or email already registered."
    }
    ```
  - `400 Bad Request` (reCAPTCHA verification failed):
    
    ```json
    {
      "detail": "reCAPTCHA verification failed."
    }
    ```

#### Usage Example

**Using `curl`:**

```bash
curl -X POST "http://localhost:8000/api/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
           "name": "John Doe",
           "email": "john.doe@example.com",
           "password": "SecurePassword123!",
           "recaptcha_token": "03AGdBq25..."
         }'
```

---

### 2.1.2 Login (`login.py`)

- **Path**: `/api/auth/login`
- **Method**: `POST`
- **Description**: Authenticates a user and returns a JWT access token.
- **Authentication**: Requires valid user credentials.

#### Request

- **Headers**:
  
  - `Content-Type: application/json`
- **Body**:
  
  ```json
  {
    "email": "john.doe@example.com",
    "password": "SecurePassword123!"
  }
  ```

#### Response

- **Status Code**: `200 OK`
- **Body**:
  
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
  ```
- **Error Responses**:
  
  - `401 Unauthorized`:
    
    ```json
    {
      "detail": "Incorrect email or password."
    }
    ```
  - `403 Forbidden`:
    
    ```json
    {
      "detail": "Email not verified."
    }
    ```

#### Usage Example

**Using `curl`:**

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
           "email": "john.doe@example.com",
           "password": "SecurePassword123!"
         }'
```

---

### 2.1.3 Email Verification (`email_verification.py`)

- **Path**: `/api/auth/verify-email`
- **Method**: `GET`
- **Description**: Verifies a user's email using a token sent via email.

#### Request

- **Query Parameters**:
  
  - `token` (string, required): The verification token.
- **Example URL**:
  
  ```
  http://localhost:8000/api/auth/verify-email?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  ```

#### Response

- **Status Code**: `200 OK`
- **Body**:
  
  ```json
  {
    "message": "Email verified successfully."
  }
  ```
- **Error Responses**:
  
  - `400 Bad Request`:
    
    ```json
    {
      "detail": "Invalid or expired token."
    }
    ```
  - `404 Not Found`:
    
    ```json
    {
      "detail": "User not found."
    }
    ```
  - `400 Bad Request` (if already verified):
    
    ```json
    {
      "message": "Email already verified."
    }
    ```

#### Usage Example

**Using a Web Browser:**

Navigate to the verification link received in the email, for example:

```
http://localhost:8000/api/auth/verify-email?token=eyJhbGciOiJIUzI1NiIsInR...
```

---

### 2.1.4 Resend Verification Email (`resend_verification.py`)

- **Path**: `/api/auth/resend-verification`
- **Method**: `POST`
- **Description**: Resends the verification email to the user, subject to a cooldown period.

#### Request

- **Headers**:
  
  - `Content-Type: application/json`
- **Body**:
  
  ```json
  {
    "email": "john.doe@example.com"
  }
  ```

#### Response

- **Status Code**: `200 OK`
- **Body**:
  
  ```json
  {
    "message": "Verification email resent successfully."
  }
  ```
- **Error Responses**:
  
  - `429 Too Many Requests`:
    
    ```json
    {
      "detail": "Please wait before requesting another verification email."
    }
    ```
  - `404 Not Found`:
    
    ```json
    {
      "detail": "User not found."
    }
    ```
  - `400 Bad Request`:
    
    ```json
    {
      "detail": "Email already verified."
    }
    ```

#### Usage Example

**Using `curl`:**

```bash
curl -X POST "http://localhost:8000/api/auth/resend-verification" \
     -H "Content-Type: application/json" \
     -d '{
           "email": "john.doe@example.com"
         }'
```

---

## 3. Admin APIs (`admin/`)

Used by administrators to manage users, review parking space submissions, and modify system configurations.

### 3.1.1 User Management (`user_management.py`)

#### 3.1.1.1 Get Users

- **Path**: `/api/admin/users`
- **Method**: `GET`
- **Description**: Retrieves a list of all users.
- **Authentication**: Admin privileges required.

#### Request

- **Headers**:
  - `Authorization: Bearer <admin_jwt_token>`

#### Response

- **Status Code**: `200 OK`
- **Body**:
  
  ```json
  [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john.doe@example.com",
      "is_verified": true,
      "is_active": true,
      "is_admin": false,
      "created_at": "2024-04-01T12:34:56Z"
    },
    {
      "id": 2,
      "name": "Jane Smith",
      "email": "jane.smith@example.com",
      "is_verified": true,
      "is_active": true,
      "is_admin": true,
      "created_at": "2024-04-02T09:20:30Z"
    }
  ]
  ```
- **Error Responses**:
  
  - `403 Forbidden`:
    
    ```json
    {
      "detail": "Not authorized to perform this action."
    }
    ```

#### Usage Example

**Using `curl`:**

```bash
curl -X GET "http://localhost:8000/api/admin/users" \
     -H "Authorization: Bearer <admin_jwt_token>"
```

---

#### 3.1.1.2 Update User Status

- **Path**: `/api/admin/users/{user_id}`
- **Method**: `PUT`
- **Description**: Updates the active status of a specified user.
- **Authentication**: Admin privileges required.

#### Request

- **Headers**:
  
  - `Authorization: Bearer <admin_jwt_token>`
  - `Content-Type: application/json`
- **Path Parameters**:
  
  - `user_id` (integer, required): ID of the user to update.
- **Body**:
  
  ```json
  {
    "is_active": false
  }
  ```

#### Response

- **Status Code**: `200 OK`
- **Body**:
  
  ```json
  {
    "message": "User status updated successfully."
  }
  ```
- **Error Responses**:
  
  - `404 Not Found`:
    
    ```json
    {
      "detail": "User not found."
    }
    ```
  - `403 Forbidden`:
    
    ```json
    {
      "detail": "Not authorized to perform this action."
    }
    ```

#### Usage Example

**Using `curl`:**

```bash
curl -X PUT "http://localhost:8000/api/admin/users/1" \
     -H "Authorization: Bearer <admin_jwt_token>" \
     -H "Content-Type: application/json" \
     -d '{"is_active": false}'
```

---

### 3.1.2 Parking Submission Management (`parking_submission_management.py`)

#### 3.1.2.1 Get Parking Submissions

- **Path**: `/api/admin/parking-submissions`
- **Method**: `GET`
- **Description**: Retrieves all parking space submissions pending review.
- **Authentication**: Admin privileges required.

#### Request

- **Headers**:
  - `Authorization: Bearer <admin_jwt_token>`

#### Response

- **Status Code**: `200 OK`
- **Body**:
  
  ```json
  [
    {
      "submission_id": 1,
      "user_id": 2,
      "address": "456 Elm Street",
      "parking_count": 15,
      "permit_required": true,
      "status": "pending",
      "submitted_at": "2024-04-10T08:45:00Z"
    },
    {
      "submission_id": 2,
      "user_id": 3,
      "address": "789 Oak Avenue",
      "parking_count": 20,
      "permit_required": false,
      "status": "pending",
      "submitted_at": "2024-04-11T14:30:00Z"
    }
  ]
  ```
- **Error Responses**:
  
  - `403 Forbidden`:
    
    ```json
    {
      "detail": "Not authorized to perform this action."
    }
    ```

#### Usage Example

**Using `curl`:**

```bash
curl -X GET "http://localhost:8000/api/admin/parking-submissions" \
     -H "Authorization: Bearer <admin_jwt_token>"
```

---

#### 3.1.2.2 Review Parking Submission

- **Path**: `/api/admin/parking-submissions/{submission_id}`
- **Method**: `PUT`
- **Description**: Approves or rejects a specific parking space submission.
- **Authentication**: Admin privileges required.

#### Request

- **Headers**:
  
  - `Authorization: Bearer <admin_jwt_token>`
  - `Content-Type: application/json`
- **Path Parameters**:
  
  - `submission_id` (integer, required): ID of the submission to review.
- **Body**:
  
  ```json
  {
    "status": "approved"
  }
  ```
  
  - **Allowed Values**: `"approved"`, `"rejected"`

#### Response

- **Status Code**: `200 OK`
- **Body**:
  
  ```json
  {
    "message": "Parking submission approved successfully."
  }
  ```
- **Error Responses**:
  
  - `400 Bad Request`:
    
    ```json
    {
      "detail": "Invalid status value."
    }
    ```
  - `404 Not Found`:
    
    ```json
    {
      "detail": "Submission not found."
    }
    ```
  - `403 Forbidden`:
    
    ```json
    {
      "detail": "Not authorized to perform this action."
    }
    ```

#### Usage Example

**Using `curl`:**

```bash
curl -X PUT "http://localhost:8000/api/admin/parking-submissions/1" \
     -H "Authorization: Bearer <admin_jwt_token>" \
     -H "Content-Type: application/json" \
     -d '{"status": "approved"}'
```

---

### 3.1.3 Configuration Management (`config_management.py`)

#### 3.1.3.1 Get System Configuration

- **Path**: `/api/admin/config`
- **Method**: `GET`
- **Description**: Retrieves the current system configuration settings.
- **Authentication**: Admin privileges required.

#### Request

- **Headers**:
  - `Authorization: Bearer <admin_jwt_token>`

#### Response

- **Status Code**: `200 OK`
- **Body**:
  
  ```json
  {
    "smtp_server": "smtp.example.com",
    "smtp_port": 587,
    "smtp_username": "no-reply@example.com",
    "smtp_sender": "no-reply@example.com",
    "frontend_url": "http://localhost:3000",
    "cooldown_period_minutes": 15
  }
  ```
- **Error Responses**:
  
  - `403 Forbidden`:
    
    ```json
    {
      "detail": "Not authorized to perform this action."
    }
    ```

#### Usage Example

**Using `curl`:**

```bash
curl -X GET "http://localhost:8000/api/admin/config" \
     -H "Authorization: Bearer <admin_jwt_token>"
```

---

#### 3.1.3.2 Update System Configuration

- **Path**: `/api/admin/config`
- **Method**: `PUT`
- **Description**: Updates specific system configuration parameters.
- **Authentication**: Admin privileges required.

#### Request

- **Headers**:
  
  - `Authorization: Bearer <admin_jwt_token>`
  - `Content-Type: application/json`
- **Body**:
  
  ```json
  {
    "config_key": "smtp_server",
    "config_value": "smtp.newserver.com"
  }
  ```
  
  - **Allowed `config_key` Values**:
    - `smtp_server`
    - `smtp_port`
    - `smtp_username`
    - `smtp_sender`
    - `frontend_url`
    - `cooldown_period_minutes`

#### Response

- **Status Code**: `200 OK`
- **Body**:
  
  ```json
  {
    "message": "Configuration updated successfully."
  }
  ```
- **Error Responses**:
  
  - `400 Bad Request`:
    
    ```json
    {
      "detail": "Invalid configuration key or value."
    }
    ```
  - `403 Forbidden`:
    
    ```json
    {
      "detail": "Not authorized to perform this action."
    }
    ```
  - `404 Not Found`:
    
    ```json
    {
      "detail": "Configuration key not found."
    }
    ```

#### Usage Example

**Using `curl`:**

```bash
curl -X PUT "http://localhost:8000/api/admin/config" \
     -H "Authorization: Bearer <admin_jwt_token>" \
     -H "Content-Type: application/json" \
     -d '{"config_key": "smtp_server", "config_value": "smtp.newserver.com"}'
```

---

## 4. Parking Spaces APIs (`parking_spaces/`)

Handles the creation, status updates, and retrieval of parking spaces.

### 4.1.1 Create Parking Space (`create_parking_space.py`)

- **Path**: `/api/parking-spaces`
- **Method**: `POST`
- **Description**: Creates a new parking space division, including address information, number of parking spots, and whether a permit is required.
- **Authentication**: Admin privileges required.

#### Request

- **Headers**:
  
  - `Authorization: Bearer <admin_jwt_token>`
  - `Content-Type: application/json`
- **Body**:
  
  ```json
  {
    "address": "123 Maple Street",
    "parking_count": 20,
    "permit_required": true
  }
  ```

#### Response

- **Status Code**: `201 Created`
- **Body**:
  
  ```json
  {
    "id": 1,
    "address": "123 Maple Street",
    "parking_count": 20,
    "permit_required": true,
    "is_full": false,
    "created_at": "2024-04-15T10:00:00Z"
  }
  ```
- **Error Responses**:
  
  - `400 Bad Request`:
    
    ```json
    {
      "detail": "Invalid input data."
    }
    ```
  - `403 Forbidden`:
    
    ```json
    {
      "detail": "Not authorized to perform this action."
    }
    ```

#### Usage Example

**Using `curl`:**

```bash
curl -X POST "http://localhost:8000/api/parking-spaces" \
     -H "Authorization: Bearer <admin_jwt_token>" \
     -H "Content-Type: application/json" \
     -d '{
           "address": "123 Maple Street",
           "parking_count": 20,
           "permit_required": true
         }'
```

---

### 4.1.2 Set Full Status (`set_full_status.py`)

- **Path**: `/api/parking-spaces/{parking_space_id}/set-full`
- **Method**: `POST`
- **Description**: Allows a user to mark a parking space as full or not full to inform other users.
- **Authentication**: User must be authenticated.

#### Request

- **Headers**:
  
  - `Authorization: Bearer <user_jwt_token>`
  - `Content-Type: application/json`
- **Path Parameters**:
  
  - `parking_space_id` (integer, required): ID of the parking space.
- **Body**:
  
  ```json
  {
    "is_full": true
  }
  ```

#### Response

- **Success (200 OK):**
  
  ```json
  {
    "message": "Parking space status updated successfully."
  }
  ```
- **Cooldown Active (429 Too Many Requests):**
  
  ```json
  {
    "detail": "Cooldown active. Please wait 4 minutes and 30 seconds before updating again."
  }
  ```
- **Parking Space Not Found (404 Not Found):**
  
  ```json
  {
    "detail": "Parking space not found."
  }
  ```
- **Unauthorized (403 Forbidden):**
  
  ```json
  {
    "detail": "Not authorized to perform this action."
  }
  ```

#### Usage Example

**Using `curl`:**

```bash
curl -X POST "http://localhost:8000/api/parking-spaces/1/set-full" \
     -H "Authorization: Bearer <user_jwt_token>" \
     -H "Content-Type: application/json" \
     -d '{"is_full": true}'
```

---

### 4.1.3 List Parking Spaces (`list_parking_spaces.py`)

- **Path**: `/api/parking-spaces`
- **Method**: `GET`
- **Description**: Retrieves a list of all parking spaces, supporting pagination.

#### Request

- **Query Parameters** (optional):
  - `page` (integer, optional): Page number (default: 1).
  - `limit` (integer, optional): Number of items per page (default: 10).

#### Response

- **Status Code**: `200 OK`
- **Body**:
  
  ```json
  {
    "parking_spaces": [
      {
        "id": 1,
        "address": "123 Maple Street",
        "parking_count": 20,
        "permit_required": true,
        "is_full": false,
        "created_at": "2024-04-15T10:00:00Z"
      },
      {
        "id": 2,
        "address": "456 Pine Avenue",
        "parking_count": 15,
        "permit_required": false,
        "is_full": true,
        "created_at": "2024-04-16T14:30:00Z"
      }
    ],
    "total": 2,
    "page": 1,
    "limit": 10
  }
  ```
- **Error Responses**:
  
  - `400 Bad Request`:
    
    ```json
    {
      "detail": "Invalid pagination parameters."
    }
    ```

#### Usage Example

**Using `curl` with Pagination:**

```bash
curl -X GET "http://localhost:8000/api/parking-spaces?page=1&limit=10"
```

---

### 4.1.4 Get Parking Space Details (`get_parking_space_details.py`)

- **Path**: `/api/parking-spaces/{parking_space_id}`
- **Method**: `GET`
- **Description**: Retrieves detailed information about a specific parking space.

#### Request

- **Path Parameters**:
  - `parking_space_id` (integer, required): ID of the parking space.

#### Response

- **Status Code**: `200 OK`
- **Body**:
  
  ```json
  {
    "id": 1,
    "address": "123 Maple Street",
    "parking_count": 20,
    "permit_required": true,
    "is_full": false,
    "created_at": "2024-04-15T10:00:00Z"
  }
  ```
- **Error Responses**:
  
  - `404 Not Found`:
    
    ```json
    {
      "detail": "Parking space not found."
    }
    ```

#### Usage Example

**Using `curl`:**

```bash
curl -X GET "http://localhost:8000/api/parking-spaces/1"
```

---

## 5. Submissions APIs (`submissions/`)

Handles user submissions for new parking space divisions, requiring authentication and admin review.

### 5.1.1 Submit Parking Space (`submit_parking_space.py`)

- **Path**: `/api/submissions/parking-spaces`
- **Method**: `POST`
- **Description**: Allows authenticated users to submit a new parking space division request for admin approval.
- **Authentication**: User must be authenticated and have passed reCAPTCHA verification during registration.

#### Request

- **Headers**:
  
  - `Authorization: Bearer <user_jwt_token>`
  - `Content-Type: application/json`
- **Body**:
  
  ```json
  {
    "address": "789 Birch Road",
    "parking_count": 25,
    "permit_required": false
  }
  ```

#### Response

- **Status Code**: `201 Created`
- **Body**:
  
  ```json
  {
    "submission_id": 3,
    "message": "Parking submission submitted successfully and is pending approval."
  }
  ```
- **Error Responses**:
  
  - `400 Bad Request`:
    
    ```json
    {
      "detail": "Submission cooldown active. Please wait before submitting again."
    }
    ```
  - `401 Unauthorized`:
    
    ```json
    {
      "detail": "Authentication credentials were not provided."
    }
    ```

#### Usage Example

**Using `curl`:**

```bash
curl -X POST "http://localhost:8000/api/submissions/parking-spaces" \
     -H "Authorization: Bearer <user_jwt_token>" \
     -H "Content-Type: application/json" \
     -d '{
           "address": "789 Birch Road",
           "parking_count": 25,
           "permit_required": false
         }'
```


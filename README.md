# fastapi-auth-drivers-api
# FastAPI Drivers API

A secure and modern REST API built with **FastAPI**, featuring JWT authentication and asynchronous database operations using SQLAlchemy.

This project demonstrates backend development skills including authentication, database modeling, and CRUD operations.

---

## Features

* User registration and login (JWT authentication)
* Secure password hashing
* Protected routes using OAuth2 Bearer token
* Async SQLAlchemy integration
* CRUD operations for drivers
* Query filtering (e.g., by city, limit results)
* Auto database table creation on startup

---

## Tech Stack

* FastAPI
* SQLAlchemy (Async)
* PostgreSQL / SQLite (depending on setup)
* Pydantic
* JWT (JSON Web Tokens)
* Python 3.10+

---

## Project Structure

```
.
├── main.py
├── models.py
├── database.py
├── auth.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/fastapi-drivers-api.git
cd fastapi-drivers-api
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set environment variables

Create a `.env` file:

```env
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite+aiosqlite:///./test.db
```

---

### 5. Run the application

```bash
uvicorn main:app --reload
```

---

## Authentication Flow

1. Register a user:

```
POST /register
```

2. Login to get token:

```
POST /login
```

3. Use token in requests:

```
Authorization: Bearer <your_token>
```

---

## API Endpoints

### Auth

* `POST /register`
* `POST /login`

### Drivers (Protected)

* `GET /drivers`
* `GET /drivers/{id}`
* `POST /drivers`

---

## Example Driver JSON

```json
{
  "name": "John Mwangi",
  "age": 30,
  "city": "Nairobi",
  "rating": 4.5
}
```

---

## Security Notes

* Passwords are hashed using secure hashing algorithms
* JWT tokens expire after 30 minutes (configurable)
* Protected routes require authentication

---

## Future Improvements

* Add update & delete driver endpoints
* Add pagination
* Add role-based access control (admin/user)
* Dockerize the application
* Add unit tests (pytest)
* Deploy to cloud (Render / AWS / Railway)

---

## Author

Built by a Data Engineering enthusiast transitioning into backend development 

# Qeja Backend — Real Estate Platform API

[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge\&logo=flask\&logoColor=white)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge\&logo=python\&logoColor=white)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge\&logo=sqlite\&logoColor=white)](https://www.sqlite.org/)
[![Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=for-the-badge\&logo=render\&logoColor=white)](https://render.com/)

A **RESTful API backend** built with **Flask**, powering the **Qeja Real Estate Platform**.
Handles authentication, property listings, messaging, social interactions, and community features.

**[Frontend Repository](https://github.com/yourusername/qeja-frontend)** •
**[Report Bug](../../issues)** • **[Request Feature](../../issues)**

---

## 📋 Table of Contents

* [About](#about)
* [Features](#features)
* [Tech Stack](#tech-stack)
* [Database Schema](#database-schema)
* [API Endpoints](#api-endpoints)
* [Getting Started](#getting-started)

  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Environment Variables](#environment-variables)
* [Project Structure](#project-structure)
* [Authentication](#authentication)
* [Deployment](#deployment)
* [Contributing](#contributing)
* [License](#license)

---

## 🎯 About

The **Qeja Backend** is a scalable Flask-based API for managing real estate operations including:

* User management
* Property listings
* Messaging
* Community posts
* Social interactions (follow, like)

Built to be secure, efficient, and suitable for production-ready deployments.

---

## ✨ Features

### Core Functionality

* 🔐 **JWT Authentication** with role-based access control
* 👤 **User Management** (profiles, activation, roles)
* 🏡 **Property Listings** with amenities & images
* 💬 **Real-Time Messaging** with optional image attachments
* 👥 **Social Features** (follow/unfollow, like properties)
* 📝 **Community Forum** with multimedia posts
* 📧 **Email Notifications** using Flask-Mail
* 🔒 **Secure Password Hashing** (Bcrypt)
* 🔄 **Database Migrations** (Flask-Migrate / Alembic)

---

## 🛠 Tech Stack

### Backend Framework

* Flask 2.x
* Flask-RESTful
* Python 3.8+

### Database & ORM

* SQLite
* SQLAlchemy
* Flask-SQLAlchemy
* SQLAlchemy-Serializer

### Authentication & Security

* Flask-JWT-Extended
* Flask-Bcrypt
* Flask-CORS

### Additional Extensions

* Flask-Mail
* Flask-Session
* Flask-Migrate
* python-dotenv

---

## 🗄 Database Schema

### User Model

Stores user authentication and profile info.

**Fields:**

* `id`, `name`, `email`, `phone`
* `password_hash`
* `role_id`
* `is_active`, `activation_code`
* `date_added`

**Relationships:**

* One-to-One: `Profile`
* One-to-Many: `Properties`, `Posts`, `Messages`
* Many-to-Many: Followers, Liked Properties

---

### Profile Model

Stores extended user details:

* `bio`, `location`, `profile_pic`
* `user_id` (FK)

---

### Property Model

Real estate listing details.

**Fields include:**

* `id`
* `pic1`, `pic2`, `pic3`
* `description`
* `location`
* `rent`
* amenity booleans (`wifi`, `gated`, `hot_shower`, etc.)
* `rooms`, `available`
* `user_id`
* `date_added`

**Relationships:**

* Many-to-One: Owner (User)
* Many-to-Many: Likers

---

### Message Model

User-to-user messages.

* `sender_id`, `receiver_id`
* `content`
* `img` (optional)
* `date_added`

---

### Post Model

Community posts.

* `id`, `user_id`
* `content`
* `pic1`, `pic2`, `pic3`
* `date_added`

---

### Role Model

Defines user roles.

* `id`
* `title`

---

### Association Tables

* `followers`: User ↔ User
* `likes`: User ↔ Properties

---

## 🔌 API Endpoints

### Authentication

| Method | Endpoint    | Description      | Auth |
| ------ | ----------- | ---------------- | ---- |
| POST   | `/login`    | Login a user     | ❌    |
| POST   | `/logout`   | Logout user      | ✔    |
| GET    | `/whoami`   | Get current user | ✔    |
| POST   | `/activate` | Activate account | ❌    |

---

### Users

| Method | Endpoint                | Description       | Auth |
| ------ | ----------------------- | ----------------- | ---- |
| GET    | `/users`                | List all users    | ✔    |
| POST   | `/users`                | Register user     | ❌    |
| GET    | `/users/<id>`           | Get user          | ✔    |
| PATCH  | `/users/<id>`           | Update user       | ✔    |
| DELETE | `/users/<id>`           | Delete user       | ✔    |
| GET    | `/users/roles/<roleId>` | Get users by role | ✔    |

---

### Properties

| Method | Endpoint           | Description     | Auth |
| ------ | ------------------ | --------------- | ---- |
| GET    | `/properties`      | All properties  | ❌    |
| POST   | `/properties`      | Create property | ✔    |
| GET    | `/properties/<id>` | Get property    | ❌    |
| PATCH  | `/properties/<id>` | Update property | ✔    |
| DELETE | `/properties/<id>` | Delete property | ✔    |

---

### Profiles

| Method | Endpoint         | Description    | Auth |
| ------ | ---------------- | -------------- | ---- |
| GET    | `/profiles`      | All profiles   | ✔    |
| POST   | `/profiles`      | Create profile | ✔    |
| GET    | `/profiles/<id>` | Get profile    | ✔    |
| PATCH  | `/profiles/<id>` | Update profile | ✔    |
| DELETE | `/profiles/<id>` | Delete profile | ✔    |

---

### Posts

| Method | Endpoint      | Description | Auth |
| ------ | ------------- | ----------- | ---- |
| GET    | `/posts`      | All posts   | ✔    |
| POST   | `/posts`      | Create post | ✔    |
| GET    | `/posts/<id>` | Get post    | ✔    |
| PATCH  | `/posts/<id>` | Update post | ✔    |
| DELETE | `/posts/<id>` | Delete post | ✔    |

---

### Social Features

| Method | Endpoint              | Description             | Auth |
| ------ | --------------------- | ----------------------- | ---- |
| POST   | `/follow/<user_id>`   | Follow a user           | ✔    |
| DELETE | `/unfollow/<user_id>` | Unfollow                | ✔    |
| GET    | `/mates`              | Get followers/following | ✔    |

---

### Messaging

| Method | Endpoint        | Description  | Auth |
| ------ | --------------- | ------------ | ---- |
| POST   | `/send-message` | Send message | ✔    |

---

### Roles

| Method | Endpoint | Description | Auth |
| ------ | -------- | ----------- | ---- |
| GET    | `/roles` | List roles  | ✔    |

---

## 🚀 Getting Started

### Prerequisites

* Python 3.8+
* pip
* Virtual environment
* SQLite (bundled with Python)

---

### Installation

```bash
git clone https://github.com/coderbenny/qeja-backend.git
cd qeja-backend
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate     # Mac/Linux
venv\Scripts\activate        # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
flask db upgrade
```

Start the development server:

```bash
flask run
```

---

### Environment Variables

Create a `.env` file:

```
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=jwt-secret-key
MAIL_USERNAME=you@example.com
MAIL_PASSWORD=yourpassword
DATABASE_URL=sqlite:///qeja.db
```

---

## 📁 Project Structure

```
qeja-backend/
│── app/
│   ├── models/
│   ├── routes/
│   ├── utils/
│   ├── __init__.py
│── migrations/
│── venv/
│── requirements.txt
│── config.py
│── run.py
│── README.md
```

---

## 🔐 Authentication

* JWT-based
* Access + Refresh tokens
* Account activation via email
* Role-based permissions

---

## 🚀 Deployment

The app can be deployed on:

* Render
* Railway
* DigitalOcean
* AWS
* Any WSGI-compatible provider

Ensure you use:

* Gunicorn
* Production configuration
* Secure environment variables

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a feature branch
3. Submit a PR

---

## 📄 License

This project is licensed under the **MIT License**.

---

If you want, I can also:

✅ Add an **OpenAPI/Swagger docs** section
✅ Generate a **Postman collection**
✅ Add **example request/response bodies**
✅ Help you create automatic **Render deployment instructions**

Just tell me!

```markdown
# Qeja Backend - Real Estate Platform API

<div align="center">

[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Deployed on Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com/)

**RESTful API backend for the Qeja real estate platform**

[Frontend Repository](https://github.com/yourusername/qeja-frontend) • [Report Bug](../../issues) • [Request Feature](../../issues)

</div>

---

## 📋 Table of Contents

- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Database Schema](#database-schema)
- [API Endpoints](#api-endpoints)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
- [Project Structure](#project-structure)
- [Authentication](#authentication)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 About

The Qeja Backend is a robust Flask-based RESTful API that powers the Qeja real estate platform. It handles user authentication, property management, messaging, social features (following/followers), and community posts. Built with scalability and security in mind, it provides a comprehensive backend solution for real estate applications.

---

## ✨ Features

### Core Functionality

- **🔐 User Authentication & Authorization**: JWT-based authentication with role-based access control
- **👤 User Management**: Registration, activation, profile management, and role assignment
- **🏡 Property Management**: CRUD operations for rental and sale properties with image support
- **💬 Real-Time Messaging**: User-to-user messaging system with image attachments
- **👥 Social Features**: Follow/unfollow users, like properties, view followers/following
- **📝 Community Forum**: Create, read, update, and delete posts with multimedia support
- **📧 Email Notifications**: Account activation and notification system via Flask-Mail
- **🔒 Password Security**: Bcrypt password hashing for secure authentication
- **🔄 Database Migrations**: Alembic/Flask-Migrate for version-controlled schema changes

---

## 🛠 Tech Stack

### Core Framework
- **Flask 2.x**: Lightweight WSGI web application framework
- **Flask-RESTful**: Extension for building REST APIs
- **Python 3.8+**: Programming language

### Database & ORM
- **SQLite**: Lightweight relational database
- **SQLAlchemy**: SQL toolkit and ORM
- **Flask-SQLAlchemy**: Flask extension for SQLAlchemy
- **SQLAlchemy-Serializer**: Automatic serialization of SQLAlchemy models

### Authentication & Security
- **Flask-JWT-Extended**: JWT token management
- **Flask-Bcrypt**: Password hashing
- **Flask-CORS**: Cross-Origin Resource Sharing support

### Additional Extensions
- **Flask-Mail**: Email sending capabilities
- **Flask-Session**: Server-side session management
- **Flask-Migrate**: Database migration handling
- **python-dotenv**: Environment variable management

---

## 🗄 Database Schema

### Models Overview

#### **User Model**
Primary user entity with authentication and profile data.

**Fields:**
- `id`: Primary key
- `name`: User's full name
- `email`: Unique email address
- `phone`: Contact number
- `password_hash`: Encrypted password
- `role_id`: Foreign key to Role
- `is_active`: Account activation status
- `activation_code`: Email verification code
- `date_added`: Registration timestamp

**Relationships:**
- One-to-One: `Profile`
- One-to-Many: `Properties`, `Posts`, `Messages` (sent/received)
- Many-to-Many: `Followers`, `Liked Properties`

#### **Profile Model**
Extended user information.

**Fields:**
- `id`: Primary key
- `bio`: User biography
- `location`: User's location
- `profile_pic`: Profile picture URL
- `user_id`: Foreign key to User

#### **Property Model**
Real estate listings.

**Fields:**
- `id`: Primary key
- `pic1`, `pic2`, `pic3`: Property images
- `description`: Property details
- `location`: Property address
- `rent`: Rental/sale price
- `wifi`, `gated`, `hot_shower`, `kitchen`, `balcony`, `parking`: Boolean amenities
- `rooms`: Number of rooms
- `available`: Availability status
- `user_id`: Property owner (Foreign key)
- `date_added`: Listing timestamp

**Relationships:**
- Many-to-One: `User` (owner)
- Many-to-Many: `Users` (likers)

#### **Message Model**
User-to-user messaging.

**Fields:**
- `id`: Primary key
- `sender_id`: Foreign key to User
- `receiver_id`: Foreign key to User
- `content`: Message text
- `img`: Optional image attachment
- `date_added`: Timestamp

#### **Post Model**
Community forum posts.

**Fields:**
- `id`: Primary key
- `user_id`: Foreign key to User
- `content`: Post content (max 255 chars)
- `pic1`, `pic2`, `pic3`: Optional images
- `date_added`: Post timestamp

#### **Role Model**
User role definitions (e.g., Admin, User, Agent).

**Fields:**
- `id`: Primary key
- `title`: Role name

### Association Tables

- **followers**: Many-to-Many relationship between Users (follower/followed)
- **likes**: Many-to-Many relationship between Users and Properties

---

## 🔌 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/login` | User login | No |
| POST | `/logout` | User logout | Yes |
| GET | `/whoami` | Get current user info | Yes |
| POST | `/activate` | Activate user account | No |

### Users

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/users` | Get all users | Yes |
| POST | `/users` | Register new user | No |
| GET | `/users/<id>` | Get user by ID | Yes |
| PATCH | `/users/<id>` | Update user | Yes |
| DELETE | `/users/<id>` | Delete user | Yes |
| GET | `/users/roles/<roleId>` | Get users by role | Yes |

### Properties

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/properties` | Get all properties | No |
| POST | `/properties` | Create property | Yes |
| GET | `/properties/<id>` | Get property by ID | No |
| PATCH | `/properties/<id>` | Update property | Yes |
| DELETE | `/properties/<id>` | Delete property | Yes |

### Profiles

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/profiles` | Get all profiles | Yes |
| POST | `/profiles` | Create profile | Yes |
| GET | `/profiles/<id>` | Get profile by ID | Yes |
| PATCH | `/profiles/<id>` | Update profile | Yes |
| DELETE | `/profiles/<id>` | Delete profile | Yes |

### Posts

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/posts` | Get all posts | Yes |
| POST | `/posts` | Create post | Yes |
| GET | `/posts/<id>` | Get post by ID | Yes |
| PATCH | `/posts/<id>` | Update post | Yes |
| DELETE | `/posts/<id>` | Delete post | Yes |

### Social Features

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/follow/<user_id>` | Follow a user | Yes |
| DELETE | `/unfollow/<user_id>` | Unfollow a user | Yes |
| GET | `/mates` | Get user's social network | Yes |

### Messaging

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/send-message` | Send message to user | Yes |

### Roles

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/roles` | Get all roles | Yes |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- SQLite (included with Python)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/qeja-backend.git
   cd qeja-backend
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your_secret_key_here
   JWT_SECRET_KEY=your_jwt_secret_key_here
   DATABASE_URL=sqlite:///qeja.db
   
   # Flask Mail Configuration
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your_email@gmail.com
   MAIL_PASSWORD=your_app_password
   MAIL_DEFAULT_SENDER=your_email@gmail.com
   
   # Flask Configuration
   FLASK_ENV=development
   FLASK_DEBUG=True
   ```

5. **Initialize the database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

   The API will be available at `http://localhost:5555`

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Flask secret key for sessions | Yes |
| `JWT_SECRET_KEY` | Secret key for JWT token generation | Yes |
| `DATABASE_URL` | Database connection string | Yes |
| `MAIL_SERVER` | SMTP server address | Yes |
| `MAIL_PORT` | SMTP server port | Yes |
| `MAIL_USE_TLS` | Enable TLS for email | Yes |
| `MAIL_USERNAME` | Email account username | Yes |
| `MAIL_PASSWORD` | Email account password/app password | Yes |
| `MAIL_DEFAULT_SENDER` | Default sender email address | Yes |
| `FLASK_ENV` | Environment (development/production) | No |
| `FLASK_DEBUG` | Enable debug mode | No |

---

## 📁 Project Structure

```
qeja-backend/
├── app.py                  # Application entry point
├── config.py               # Configuration settings
├── extensions.py           # Flask extensions initialization
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in repo)
├── lib/
│   ├── __init__.py
│   └── models.py          # SQLAlchemy models
├── routes/
│   ├── __init__.py
│   ├── Index.py           # Root endpoint
│   ├── Login.py           # Authentication routes
│   ├── Logout.py
│   ├── Whoami.py
│   ├── Activation.py
│   ├── Roles.py           # Role management
│   ├── UsersByRole.py
│   ├── FollowUser.py      # Social features
│   ├── UnfollowUser.py
│   ├── SendMessage.py     # Messaging
│   ├── UsersRsc.py        # User CRUD (Blueprint)
│   ├── PropertiesRsc.py   # Property CRUD (Blueprint)
│   ├── ProfilesRsc.py     # Profile CRUD (Blueprint)
│   ├── PostsRsc.py        # Post CRUD (Blueprint)
│   └── MatesRsc.py        # Social network (Blueprint)
└── migrations/            # Database migrations
```

---

## 🔐 Authentication

The API uses **JWT (JSON Web Tokens)** for authentication.

### Authentication Flow

1. **Registration**: POST to `/users` with user details
2. **Activation**: POST to `/activate` with activation code sent via email
3. **Login**: POST to `/login` with credentials
4. **Access Protected Routes**: Include JWT token in Authorization header

### Using JWT Tokens

Include the JWT token in the Authorization header for protected routes:

```bash
Authorization: Bearer <your_jwt_token>
```

### Example Login Request

```bash
curl -X POST http://localhost:5555/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "your_password"
  }'
```

### Example Protected Request

```bash
curl -X GET http://localhost:5555/whoami \
  -H "Authorization: Bearer <your_jwt_token>"
```

---

## 🌐 Deployment

### Deploying to Render

1. **Create a new Web Service on Render**

2. **Configure Build & Start Commands**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

3. **Add Environment Variables**
   - Add all variables from your `.env` file in the Render dashboard

4. **Add Gunicorn to requirements.txt**
   ```
   gunicorn==20.1.0
   ```

5. **Database Considerations**
   - For production, consider upgrading from SQLite to PostgreSQL
   - Update `DATABASE_URL` to PostgreSQL connection string

### Production Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Set `FLASK_DEBUG=False`
- [ ] Use strong, unique `SECRET_KEY` and `JWT_SECRET_KEY`
- [ ] Configure production database (PostgreSQL recommended)
- [ ] Set up proper CORS origins
- [ ] Configure email service for production
- [ ] Enable HTTPS
- [ ] Set up logging and monitoring
- [ ] Implement rate limiting
- [ ] Configure backup strategy

---

## 🧪 Testing

```bash
# Run tests (once test suite is implemented)
python -m pytest

# Run with coverage
python -m pytest --cov=.
```

---

## 📦 Dependencies

### Core Requirements

```
Flask==2.3.0
Flask-RESTful==0.3.10
Flask-SQLAlchemy==3.0.5
Flask-JWT-Extended==4.5.2
Flask-Bcrypt==1.0.1
Flask-CORS==4.0.0
Flask-Mail==0.9.1
Flask-Session==0.5.0
Flask-Migrate==4.0.4
SQLAlchemy==2.0.19
SQLAlchemy-serializer==1.4.1
python-dotenv==1.0.0
```

See `requirements.txt` for full list of dependencies.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**

2. **Create a feature branch**
   ```bash
   git checkout -b feature/YourFeatureName
   ```

3. **Commit your changes**
   ```bash
   git commit -m 'Add some feature'
   ```

4. **Push to the branch**
   ```bash
   git push origin feature/YourFeatureName
   ```

5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Write descriptive commit messages
- Add docstrings to new functions and classes
- Update documentation for new features
- Ensure all tests pass before submitting PR
- Keep pull requests focused and atomic

---

## 🐛 Known Issues & Limitations

- SQLite is used for development; consider PostgreSQL for production
- No rate limiting implemented yet
- Image storage currently uses URLs; consider implementing cloud storage
- Email activation codes are numeric; consider using token-based activation

---

## 🗺 Roadmap

- [ ] Implement comprehensive test suite
- [ ] Add API rate limiting
- [ ] Integrate cloud storage for images (AWS S3/Cloudinary)
- [ ] Add WebSocket support for real-time messaging
- [ ] Implement advanced search and filtering
- [ ] Add payment gateway integration
- [ ] Implement caching with Redis
- [ ] Add API documentation with Swagger/OpenAPI
- [ ] Set up CI/CD pipeline
- [ ] Implement logging and monitoring

---

## 📄 License

Distributed under the MIT License. See `LICENSE` file for more information.

---

## 📧 Contact

Project Link: [https://github.com/yourusername/qeja-backend](https://github.com/yourusername/qeja-backend)

Frontend Repository: [https://github.com/yourusername/qeja-frontend](https://github.com/yourusername/qeja-frontend)

---

## 🙏 Acknowledgments

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://www.sqlalchemy.org/)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- [Flask-RESTful](https://flask-restful.readthedocs.io/)
- [Render](https://render.com/)

---

<div align="center">

**Built with 🐍 and Flask**

⭐ Star this repo if you find it helpful!

[Frontend](https://github.com/coderbenny/Qeja-backend) • [Live Demo](https://qeja-frontend.vercel.app) • [API Documentation](#api-endpoints)

</div>
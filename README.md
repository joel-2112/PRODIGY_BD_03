Task03: Django Authentication and Caching API
This project, task03, is a Django REST Framework (DRF) application with an app named base. It implements a user authentication system using JSON Web Tokens (JWT) and integrates Redis caching to optimize API performance. The application includes user registration, login, profile retrieval, and a user list endpoint with role-based access control.

Features
Authentication and Authorization:
User registration with hashed passwords using bcrypt.
JWT-based authentication using djangorestframework-simplejwt.
Custom User model with roles (admin, user, owner).
Protected endpoints requiring authentication.
Role-based access control (e.g., only admins can view all users).
Caching:
Redis integration for caching frequently accessed data.
Caches the user list endpoint (/api/users/) for 15 minutes.
Performance optimization measurable via benchmarking.
Endpoints:
POST /api/register/: Register a new user.
POST /api/login/: Login and obtain JWT tokens.
POST /api/token/refresh/: Refresh an access token.
GET /api/profile/: Retrieve the authenticated user's profile.
GET /api/users/: List all users (admin-only, cached).
Prerequisites
Python 3.8+
Redis Server
Git (optional, for cloning the repository)
Setup Instructions
1. Clone the Repository (if applicable)
If you have a repository, clone it:

bash

Collapse

Wrap

Copy
git clone <repository-url>
cd task03
2. Install Dependencies
Create a virtual environment and install the required packages:

bash

Collapse

Wrap

Copy
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install django djangorestframework djangorestframework-simplejwt bcrypt redis django-redis
3. Install and Run Redis
Ubuntu/Debian:
bash

Collapse

Wrap

Copy
sudo apt-get install redis-server
redis-server
Windows: Download and install Redis from here or use WSL.
MacOS:
bash

Collapse

Wrap

Copy
brew install redis
redis-server
Verify Redis is running:
bash

Collapse

Wrap

Copy
redis-cli ping
Should return PONG.
4. Configure the Project
The project is pre-configured in task03/settings.py. Ensure the following settings are correct:

AUTH_USER_MODEL = 'base.User'
Redis cache settings:
python

Collapse

Wrap

Copy
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
5. Apply Migrations
Initialize the database:

bash

Collapse

Wrap

Copy
python manage.py makemigrations
python manage.py migrate
6. Create a Superuser (Optional)
Create an admin user for testing:

bash

Collapse

Wrap

Copy
python manage.py createsuperuser
7. Run the Development Server
Start the Django development server:

bash

Collapse

Wrap

Copy
python manage.py runserver
The API will be available at http://127.0.0.1:8000/.

Usage Examples
Register a User
bash

Collapse

Wrap

Copy
curl -X POST http://127.0.0.1:8000/api/register/ \
-H "Content-Type: application/json" \
-d '{"username": "testuser", "email": "test@example.com", "password": "securepassword123", "role": "user"}'
Login
bash

Collapse

Wrap

Copy
curl -X POST http://127.0.0.1:8000/api/login/ \
-H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "securepassword123"}'
Response:

json

Collapse

Wrap

Copy
{
    "refresh": "<refresh_token>",
    "access": "<access_token>",
    "user": {
        "id": 1,
        "username": "testuser",
        "role": "user"
    }
}
Refresh Token
bash

Collapse

Wrap

Copy
curl -X POST http://127.0.0.1:8000/api/token/refresh/ \
-H "Content-Type: application/json" \
-d '{"refresh": "<refresh_token>"}'
Get Profile
bash

Collapse

Wrap

Copy
curl -X GET http://127.0.0.1:8000/api/profile/ \
-H "Authorization: Bearer <access_token>"
Response:

json

Collapse

Wrap

Copy
{
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "role": "user"
}
Get All Users (Admin Only)
bash

Collapse

Wrap

Copy
curl -X GET http://127.0.0.1:8000/api/users/ \
-H "Authorization: Bearer <admin_access_token>"
Response:

json

Collapse

Wrap

Copy
[
    {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "role": "user"
    },
    {
        "id": 2,
        "username": "adminuser",
        "email": "admin@example.com",
        "role": "admin"
    }
]
Measuring Performance Improvements
Benchmark Script
Create a file named benchmark.py:

python

Collapse

Wrap

Copy
import requests
import time

url = 'http://127.0.0.1:8000/api/users/'
headers = {'Authorization': 'Bearer <your_admin_access_token>'}

# Without cache (first request)
start_time = time.time()
response = requests.get(url, headers=headers)
print(f"First request (no cache): {time.time() - start_time} seconds")

# With cache (second request)
start_time = time.time()
response = requests.get(url, headers=headers)
print(f"Second request (cached): {time.time() - start_time} seconds")
Run the script:

bash

Collapse

Wrap

Copy
python benchmark.py
The first request will hit the database (slower).
The second request will use the cache (faster).
Project Structure
text

Collapse

Wrap

Copy
task03/
├── base/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── task03/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── README.md
Notes
Cache Invalidation: The current implementation does not include update or delete endpoints, so cache invalidation is not implemented. If you add such endpoints, include cache.delete('all_users') in the respective views.
Security: For production, configure HTTPS, use environment variables for sensitive settings, and set DEBUG = False in settings.py.
Database: This project uses SQLite for simplicity. For production, consider using PostgreSQL or another robust database.
Redis Configuration: Ensure Redis is running on 127.0.0.1:6379. Adjust the CACHES setting if your Redis server is on a different host or port.
Contributing
Feel free to fork this repository, submit pull requests, or open issues for bugs or feature requests.

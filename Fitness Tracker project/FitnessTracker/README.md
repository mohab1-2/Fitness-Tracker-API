# Fitness Tracker API

A comprehensive Django REST Framework API for tracking fitness activities, built with authentication, CRUD operations, and analytics features.

## Features

- **User Management**: Registration, authentication, and profile management
- **Activity CRUD**: Create, read, update, and delete fitness activities
- **Activity History**: View activity history with filtering options
- **Activity Metrics**: Get summary statistics and trends
- **Authentication**: Token-based authentication
- **Pagination**: Built-in pagination for large datasets
- **Validation**: Comprehensive input validation
- **Admin Interface**: Django admin for data management

## Activity Types

- Running
- Cycling
- Weightlifting
- Swimming
- Walking
- Yoga
- Other

## API Endpoints

### Authentication

#### Register User
```
POST /api/auth/register/
Content-Type: application/json

{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123"
}
```

#### Login
```
POST /api/auth/login/
Content-Type: application/json

{
    "username": "john_doe",
    "password": "securepassword123"
}
```

#### User Profile
```
GET /api/auth/profile/
Authorization: Token <your_token>
```

### Activities

#### List/Create Activities
```
GET /api/activities/
Authorization: Token <your_token>

POST /api/activities/
Authorization: Token <your_token>
Content-Type: application/json

{
    "activity_type": "running",
    "duration": 30,
    "distance": 5.2,
    "calories_burned": 320,
    "date": "2024-01-15T10:30:00Z"
}
```

#### Activity Detail
```
GET /api/activities/{id}/
PUT /api/activities/{id}/
DELETE /api/activities/{id}/
Authorization: Token <your_token>
```

#### Activity History (with filters)
```
GET /api/activities/history/?start_date=2024-01-01&end_date=2024-01-31&activity_type=running
Authorization: Token <your_token>
```

#### Activity Metrics
```
GET /api/activities/metrics/?start_date=2024-01-01&end_date=2024-01-31
Authorization: Token <your_token>
```

#### Activity Trends
```
GET /api/activities/trends/
Authorization: Token <your_token>
```

## Setup Instructions

### 1. Clone and Navigate
```bash
cd "Fitness Tracker project/FitnessTracker"
```

### 2. Create Virtual Environment
```bash
python -m venv myenv
myenv\Scripts\activate  # Windows
# or
source myenv/bin/activate  # Linux/Mac
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

## Database Schema

### User Model
- `username` (unique)
- `email` (unique)
- `password` (hashed)
- Standard Django user fields

### Activity Model
- `user` (ForeignKey to User)
- `activity_type` (choices: running, cycling, etc.)
- `duration` (minutes, positive integer)
- `distance` (decimal, km/miles)
- `calories_burned` (positive integer)
- `date` (datetime)
- `created_at` (auto timestamp)
- `updated_at` (auto timestamp)

## Authentication

The API uses Django REST Framework's Token Authentication. Include the token in the Authorization header:

```
Authorization: Token <your_token>
```

## Validation Rules

- **Duration**: Must be positive integer
- **Distance**: Must be non-negative decimal
- **Calories**: Must be non-negative integer
- **Activity Type**: Must be one of the predefined choices
- **Date**: Must be valid datetime
- **Username/Email**: Must be unique

## Filtering and Pagination

### Activity History Filters
- `start_date`: Filter activities from this date (YYYY-MM-DD)
- `end_date`: Filter activities until this date (YYYY-MM-DD)
- `activity_type`: Filter by specific activity type

### Pagination
- Default page size: 20 items
- Use `?page=<number>` for pagination

## Example Usage

### 1. Register a new user
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "fitness_user",
    "email": "user@example.com",
    "password": "mypassword123",
    "password_confirm": "mypassword123"
  }'
```

### 2. Login and get token
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "fitness_user",
    "password": "mypassword123"
  }'
```

### 3. Create an activity
```bash
curl -X POST http://localhost:8000/api/activities/ \
  -H "Authorization: Token <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "activity_type": "running",
    "duration": 45,
    "distance": 8.5,
    "calories_burned": 450,
    "date": "2024-01-15T07:00:00Z"
  }'
```

### 4. Get activity metrics
```bash
curl -X GET "http://localhost:8000/api/activities/metrics/?start_date=2024-01-01&end_date=2024-01-31" \
  -H "Authorization: Token <your_token>"
```

## Deployment

### Heroku Deployment
1. Create a `Procfile`:
```
web: gunicorn FitnessTracker.wsgi --log-file -
```

2. Set environment variables:
```bash
heroku config:set SECRET_KEY=your_secret_key
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=your-app.herokuapp.com
```

3. Deploy:
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### PythonAnywhere Deployment
1. Upload your code to PythonAnywhere
2. Set up a virtual environment
3. Install requirements
4. Configure WSGI file
5. Set up static files

## Testing

Run the test suite:
```bash
python manage.py test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

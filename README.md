CampusCare

A College Grievance Management System built using Django and PostgreSQL.

Requirements

- Python 3.12
- PostgreSQL
- Git

Setup Instructions

1. Clone the repository

git clone https://github.com/joann16082006/CampusCare.git
cd CampusCare

2. Create and activate a virtual environment (Windows)

python -m venv venv
venv\Scripts\Activate.ps1

3. Install dependencies

pip install -r requirements.txt

4. Create a PostgreSQL database

Create a database named "campuscare_db" in PostgreSQL.

5. Configure environment variables

Create a ".env" file in the project root with your own PostgreSQL credentials:

DB_NAME=campuscare_db
DB_USER=your_postgres_username
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432

Replace the username and password with your local PostgreSQL credentials. Do not upload ".env" to GitHub.

6. Apply migrations

python manage.py migrate

7. Start the development server

python manage.py runserver

Open http://127.0.0.1:8000/login/ in your browser.

Features

- Student and staff registration and login
- Role-based access control
- User profile page
- Submit grievances
- View submitted grievances and their status
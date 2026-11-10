# Project
### This project is a modern travel agency website based on some business logic using Python and Django framework

1. Features
- User authentication and authorization -login and register
- Display travel destinations
- Browse available travel offers.
- Booking system
- Review section-users can create or delete review
- Messages section 
- Responsive design
- Newsletter subscription using EmailJS integration

2. Technologies Used
- Python
- Django
- HTML
- CSS
- JavaScript
- PostgreSQL
- Pillow

3. Project Structure
```text
project_django/
│
├── travel_agency_project/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── travel_app/
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── admin.py
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── manage.py
├── requirements.txt
├── .env
├── .gitignore
├── LICENSE
└── README.md
```
4. Installation and Setup
Make sure you have installed:
- Python
- pip library
- Git
- PostGreSQL
# Setup
1.Clone the repository
    ```bash
git clone https://github.com/megicereni/project_django ```
2.Navigate to the project directory
  ```bash
cd project_django
3.Create a virtual environment
   ```bash
python -m venv venv 
4.Activate the environment
   ```bash
venv\Scripts\activate
5.Install dependencies in the requirements file
   ```bash
pip install -r requirements.txt
6.Apply database migrations
   ```bash
python manage.py migrate
7.Start the server
   ```bash
python manage.py runserver


5.Database Configuration
This project uses PostgreSQL as its database management system.

To configure the database connection, follow these steps:
-Create .env file in the root of project
-Create some of the environments variables(
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
)
-Replace the example values with your actual PostgreSQL database credentials
-Make sure the PostgreSQL server is running
-Apply the database migrations










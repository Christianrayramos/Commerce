# CS50 Commerce
## An eBay-style auction marketplace built with Django

### Overview
This project is part of Harvard's CS50 web programming with Python and Javascript course. 
It implements a full online marketplace where users can create listings. place bids, comment on items and manage watchlists.

### Features 
- User registration, login, and session management
- Create, edit, and close auction listings
- Place bids with validation ensuring only higher bids are accepted
- Add and remove items from a personal watchlist
- Comment system for listing pages
- Category browsing for listings
- Automatic auction winner determination when a listing is closed

## Technologies Used 
- Python / Django
- HTML,CSS,Bootstrap
- SQLite
- Django ORM and templates

## How to Run this Application
- Clone the repository to your local machine and navigate into the project directory
- Install dependencies listed in the requirements.txt file by running pip install -r requirements.txt.
- Apply database migrations using python manage.py makemigrations followed by python manage.py migrate.
- Start the development server by running python manage.py runserver.
- Open your browser and go to http://127.0.0.1:8000/ to access the app.
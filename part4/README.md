# HBnB - Simple Web Client

## Overview

This project is a simple front-end web client for the HBnB platform, part of the Holberton School curriculum. It interacts with a RESTful API to allow users to log in, browse places, view details, and add reviews. The goal is to build a dynamic and user-friendly interface using vanilla JavaScript, HTML, and CSS.

## Objectives

- Create a functional front-end client using HTML, CSS, and JavaScript.
- Interact with a REST API for authentication, data fetching, and data submission.
- Dynamically display places and reviews.
- Implement login/logout functionality with cookie-based JWT handling.
- Submit reviews securely using the authenticated session.

## Features

- User login/logout with access token stored as a cookie.
- Dynamic display of places fetched from the back-end.
- Filter places by price using a dropdown.
- View detailed information about each place.
- Submit reviews with rating and comment (only when logged in).
- Redirect logic based on authentication status.

## API Endpoint used

All features are powered by a custom REST API hosted on the back-end. Key endpoints include:

- `POST /api/v1/auth/login/` — Authenticate user and receive JWT.
- `GET /api/v1/places/` — Retrieve list of available places.
- `GET /api/v1/places/<place_id>/` — Retrieve detailed information for a place.
- `POST /api/v1/reviews/` — Submit a review (authenticated).
- `GET /api/v1/reviews/?place_id=<id>` — Fetch reviews for a place.

## Screenshot

_SOON._

## Requirements

- A modern browser (Chrome, Firefox, Edge, etc.)
- The back-end API must be running and accessible (Flask + DB)
- A local development server (optional but recommended)
- Python 3.8+
- Flask
- Flask-RESTful
- SQLAlchemy (or your ORM)
- MySQL, SQLite or PostgreSQL

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/holbertonschool-hbnb.git
cd hbnb/part4
```

2. Install back-end dependencies:

```
cd hbnb
pip install -r requirements.txt
```

3. Start the back-end API server:

```
python3 run.py
```

4. Populate the database (in a second terminal):

```
sqlite3 instance/development.db < SQL_Scripts/Initial_data.sql
```

> The test admin email is :
- "Email: admin@hbnb.io"
- "Password: admin1234"

5. Start the front-end server (in a third terminal):

```
# Install http-server if you don't have it
npm install -g http-server

# Run the front-end server
npx http-server -p 5500
```

6. Open the application:
```
Navigate to http://localhost:5500/Front/landing.html in your browser.
```

## Test the features

1. Navigate to `login.html` and use your credentials to log in.
2. Browse the list of places on `index.html`.
3. Click “Details” on any place to view full info.
4. On the detail page, write and submit a review if authenticated on the place that you don't own.

## Technologies used

Front-end :  
- HTML5
- CSS3
- JavaScript (Vanilla)  
Back-end :  
- Fetch API
- REST API (Flask back-end)
- JWT for authentication
- Flask
- SQLAlchemy
- SQLite

## Author

- Benjamin Estrada

---

Project completed as part of Holberton School curriculum.

# Phase 3 – Project Design Phase

## Project Title

PocketSmart AI: Your Smart Budget & Recommendation Assistant

## System Architecture

The application follows a modular web application architecture.

User
|
v
HTML/CSS Frontend
|
v
FastAPI Backend
|
+--------------------+
|                    |
v                    v
SQLite Database    Gemini AI
|                    |
+---------+----------+
          |
          v
Budget Analysis
          |
          v
Smart Recommendations
          |
          v
User Result

## Main Modules

### app.py

The app.py file controls the main FastAPI application.

It handles:

- Web page routing
- User registration
- User login
- Logout
- Dashboard
- Budget generation
- API endpoints
- CORS
- Static files

### database.py

The database.py file handles SQLite database operations.

It manages:

- User creation
- User authentication
- Password hashing
- Budget storage
- Budget history

### gemini_service.py

The gemini_service.py file handles Gemini AI integration.

It provides:

- Gemini API connection
- AI budget analysis
- Model fallback
- Local fallback recommendation
- Gemini connection testing

### models.py

The models.py file contains data validation models used by the API.

### HTML Templates

Jinja2 templates provide the web interface.

The templates include:

- Home page
- Registration page
- Login page
- Dashboard
- Result page

### CSS

CSS is used to provide the visual design and responsive layout.

## Database Design

### Users Table

The users table stores:

- User ID
- Name
- Email
- Password hash
- Account creation date

### Budgets Table

The budgets table stores:

- Budget ID
- User ID
- Monthly income
- Expense categories
- Savings goal
- AI recommendation
- Creation date

## User Flow

Register
|
v
Login
|
v
Dashboard
|
v
Enter Budget
|
v
FastAPI
|
v
Budget Calculation
|
v
Gemini AI
|
v
Recommendation
|
v
SQLite Storage
|
v
Result Display

## Design Goals

- Simple interface
- Modular architecture
- Easy maintenance
- Mobile-friendly design
- Secure password storage
- AI-powered recommendations
- Reliable error handling

## Conclusion

The project design separates the application into independent modules, making the system easier to develop, test, maintain, and demonstrate.

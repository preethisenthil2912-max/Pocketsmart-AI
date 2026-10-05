# Phase 2 – Requirement Analysis

## Project Title

PocketSmart AI: Your Smart Budget & Recommendation Assistant

## Functional Requirements

### 1. User Registration

The system should allow a new user to create an account using their name, email, and password.

### 2. User Login

The system should allow registered users to log in using their email and password.

### 3. Budget Input

The user should be able to enter:

- Monthly income
- Rent or housing expenses
- Food expenses
- Transport expenses
- Utility expenses
- Education expenses
- Healthcare expenses
- Entertainment expenses
- Other expenses
- Savings goal

### 4. Budget Calculation

The application should calculate the total listed expenses and estimated remaining balance.

### 5. AI Budget Analysis

Gemini AI should analyze the user's budget and provide practical recommendations.

### 6. Savings Recommendation

The application should compare the user's remaining balance with the savings goal.

### 7. Database Storage

User information and budget analysis should be stored in SQLite.

### 8. Budget History

The user should be able to view previously saved budget entries.

### 9. API

The application should provide API endpoints for budget analysis, health checking, and Gemini status.

## Non-Functional Requirements

### Usability

The application should have a simple and user-friendly interface.

### Performance

The application should respond quickly under normal usage.

### Security

Passwords should not be stored as plain text.

The Gemini API key should not be stored inside the source code.

### Reliability

The application should handle Gemini API failures using model fallback and local budget calculation.

### Maintainability

The project should be divided into separate modules for:

- FastAPI application
- Database
- Gemini service
- Data models
- HTML templates
- CSS

## Hardware Requirements

- Smartphone, tablet, or computer
- Internet connection

## Software Requirements

- Python
- FastAPI
- Uvicorn
- Google Gemini AI
- Google GenAI Python SDK
- SQLite
- Jinja2
- HTML
- CSS
- GitHub Codespaces or local development environment

## Conclusion

The requirement analysis defines the functional and non-functional requirements needed to develop PocketSmart AI as a practical AI-powered budgeting web application.

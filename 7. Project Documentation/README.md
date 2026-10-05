# Phase 7 – Project Documentation

## Project Title

PocketSmart AI: Your Smart Budget & Recommendation Assistant

## Project Purpose

PocketSmart AI is an AI-powered web application designed to help users analyze their monthly income and expenses.

The application provides practical budgeting and savings recommendations.

## Technology Used

- Python
- FastAPI
- Google Gemini AI
- Google GenAI Python SDK
- SQLite
- Jinja2
- HTML5
- CSS3
- Uvicorn

## Application Modules

### Authentication Module

Provides user registration and login functionality.

### Budget Module

Accepts monthly income, expenses, and savings goals.

### AI Module

Uses Gemini AI to analyze the budget and generate recommendations.

### Database Module

Uses SQLite to store user and budget information.

### Frontend Module

Provides the web interface using HTML, Jinja2, and CSS.

## Security

Passwords are stored using password hashing.

The Gemini API key should be stored as an environment variable and should not be uploaded to GitHub.

## AI Processing

The user's budget information is processed by Gemini AI to generate recommendations.

The application also contains a fallback mechanism for Gemini model failures.

## Output

The application provides:

- Income summary
- Expense analysis
- Remaining balance
- Savings goal comparison
- Spending recommendations
- Savings suggestions

## Limitations

PocketSmart AI provides general budgeting guidance.

It does not guarantee financial results and does not replace professional financial advice.

## Future Enhancements

Future versions could include:

- Expense charts
- Monthly reports
- Downloadable reports
- Budget alerts
- Recurring expenses
- Advanced analytics
- Improved authentication
- Multiple currency support

## Conclusion

The documentation describes the design, implementation, functionality, testing, and future scope of PocketSmart AI.

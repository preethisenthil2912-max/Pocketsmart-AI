# Phase 6 – Project Testing

## Project Title

PocketSmart AI: Your Smart Budget & Recommendation Assistant

## Testing Objective

The purpose of testing is to verify that the application works correctly and handles valid and invalid user inputs.

## Test Case 1 – User Registration

Input:

Name: Test User

Email: test@example.com

Password: test1234

Expected Result:

A new account should be created successfully.

## Test Case 2 – User Login

Input:

Registered email and password.

Expected Result:

The user should be redirected to the dashboard.

## Test Case 3 – Budget Analysis

Example:

Monthly Income: ₹30000

Rent: ₹8000

Food: ₹5000

Transport: ₹2500

Utilities: ₹2000

Education: ₹2000

Healthcare: ₹1000

Entertainment: ₹1500

Other: ₹1000

Savings Goal: ₹5000

Expected Result:

The application should analyze the budget and generate recommendations.

## Test Case 4 – Invalid Income

Input:

Zero or negative income.

Expected Result:

The application should reject the invalid value.

## Test Case 5 – Gemini Status

URL:

/api/gemini-status

Expected Result:

The endpoint should report the Gemini connection status.

## Test Case 6 – Health Check

URL:

/api/health

Expected Result:

The application should return a running status.

## Test Case 7 – Database

After generating a budget, the information should be stored in SQLite.

## Test Case 8 – Mobile Interface

The application should remain usable on a mobile device.

## Test Case 9 – Gemini Failure

If the primary Gemini model is unavailable, the application should attempt another configured model.

If Gemini is unavailable, the application should use the local fallback budget recommendation.

## Conclusion

Testing verifies the major features of PocketSmart AI including authentication, budget calculation, AI recommendation, database storage, API functionality, and error handling.

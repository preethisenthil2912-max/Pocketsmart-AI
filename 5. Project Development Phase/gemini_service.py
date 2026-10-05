import os
import time

from google import genai


GEMINI_MODELS = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite"
]


def get_client():

    api_key = os.getenv(
        "GEMINI_API_KEY"
    )

    if not api_key:

        return None

    return genai.Client(
        api_key=api_key
    )


def fallback_recommendation(
    data: dict,
    user_name: str
):

    income = data["monthly_income"]

    expenses = (
        data["rent"]
        + data["food"]
        + data["transport"]
        + data["utilities"]
        + data["education"]
        + data["healthcare"]
        + data["entertainment"]
        + data["other"]
    )

    balance = income - expenses

    savings_goal = data["savings_goal"]

    if balance < 0:

        status = (
            "Your listed expenses are higher "
            "than your income. Reduce "
            "non-essential spending first."
        )

    elif balance >= savings_goal:

        status = (
            f"Your current balance can cover "
            f"the requested savings goal of "
            f"₹{savings_goal:,.0f}."
        )

    else:

        status = (
            "Your current balance is below "
            "the requested savings goal. "
            "Consider reducing flexible expenses."
        )

    return f"""
PocketSmart Budget Summary for {user_name}

Monthly income: ₹{income:,.2f}

Total listed expenses: ₹{expenses:,.2f}

Estimated balance: ₹{balance:,.2f}

Savings goal: ₹{savings_goal:,.2f}

Assessment:

{status}

Recommendations:

1. Track essential and non-essential expenses separately.

2. Set aside a fixed savings amount after receiving income.

3. Review food, entertainment and other flexible expenses.

4. Maintain an emergency fund.

5. Review your budget every month.

Note:
This is general budgeting guidance and not professional financial advice.
"""


def generate_budget_recommendation(
    data: dict,
    user_name: str = "User"
):

    client = get_client()

    if client:

        prompt = f"""
You are PocketSmart AI, a budgeting assistant.

Create a practical monthly budget analysis for {user_name}.

Monthly income: ₹{data["monthly_income"]}

Rent: ₹{data["rent"]}

Food: ₹{data["food"]}

Transport: ₹{data["transport"]}

Utilities: ₹{data["utilities"]}

Education: ₹{data["education"]}

Healthcare: ₹{data["healthcare"]}

Entertainment: ₹{data["entertainment"]}

Other expenses: ₹{data["other"]}

Savings goal: ₹{data["savings_goal"]}

Requirements:

1. Calculate total expenses.

2. Calculate estimated remaining balance.

3. Compare the balance with the savings goal.

4. Identify major spending categories.

5. Suggest practical ways to reduce unnecessary spending.

6. Give a simple savings strategy.

7. Give 3 to 5 practical recommendations.

8. Use Indian Rupees.

9. Do not request bank account numbers, passwords or OTPs.

10. Do not present financial outcomes as guaranteed.

11. State that this is general budgeting guidance.

Return only the budget analysis and recommendations.
"""

        for model_name in GEMINI_MODELS:

            try:

                print(
                    f"Trying Gemini model: {model_name}"
                )

                response = (
                    client.models.generate_content(
                        model=model_name,
                        contents=prompt
                    )
                )

                if response.text:

                    print(
                        f"Success with model: {model_name}"
                    )

                    return response.text

            except Exception as error:

                print(
                    f"Model {model_name} failed: {error}"
                )

                time.sleep(1)

    return fallback_recommendation(
        data,
        user_name
    )


def validate_gemini_connection():

    client = get_client()

    if not client:

        return (
            False,
            "GEMINI_API_KEY is not configured."
        )

    try:

        response = (
            client.models.generate_content(
                model=GEMINI_MODELS[0],
                contents=(
                    "Reply with exactly: "
                    "PocketSmart Gemini connection successful."
                )
            )
        )

        if response.text:

            return (
                True,
                response.text.strip()
            )

        return (
            False,
            "Gemini returned an empty response."
        )

    except Exception as error:

        return (
            False,
            str(error)
  )

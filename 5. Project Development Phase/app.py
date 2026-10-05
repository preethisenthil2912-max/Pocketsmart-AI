import os

from fastapi import (
    FastAPI,
    Form,
    Request
)

from fastapi.responses import (
    HTMLResponse,
    RedirectResponse
)

from fastapi.templating import (
    Jinja2Templates
)

from fastapi.staticfiles import (
    StaticFiles
)

from starlette.middleware.cors import (
    CORSMiddleware
)

from starlette.middleware.sessions import (
    SessionMiddleware
)

from database import (
    create_database,
    create_user,
    get_user_by_email,
    get_user_by_id,
    get_user_budgets,
    save_budget,
    verify_password
)

from gemini_service import (
    generate_budget_recommendation,
    validate_gemini_connection
)

from models import (
    BudgetRequest,
    RecommendationRequest
)


app = FastAPI(
    title="PocketSmart AI",
    description=(
        "AI-powered smart budget "
        "and recommendation assistant"
    ),
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv(
        "SESSION_SECRET",
        "pocketsmart-demo-session-secret"
    ),
    max_age=60 * 60 * 24
)


templates = Jinja2Templates(
    directory="templates"
)


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


create_database()


def current_user(request: Request):

    user_id = request.session.get(
        "user_id"
    )

    if not user_id:

        return None

    return get_user_by_id(
        int(user_id)
    )


@app.get(
    "/",
    response_class=HTMLResponse
)
async def home(request: Request):

    user = current_user(request)

    if user:

        return RedirectResponse(
            "/dashboard",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )


@app.get(
    "/register",
    response_class=HTMLResponse
)
async def register_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={
            "request": request,
            "error": None
        }
    )


@app.post(
    "/register",
    response_class=HTMLResponse
)
async def register(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):

    name = name.strip()
    email = email.strip().lower()

    if (
        len(name) < 2
        or len(password) < 6
        or "@" not in email
    ):

        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "request": request,
                "error": (
                    "Enter a valid name, email "
                    "and password of at least "
                    "6 characters."
                )
            },
            status_code=400
        )

    user_id = create_user(
        name,
        email,
        password
    )

    if user_id is None:

        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "request": request,
                "error": (
                    "An account with this "
                    "email already exists."
                )
            },
            status_code=400
        )

    request.session["user_id"] = int(
        user_id
    )

    return RedirectResponse(
        "/dashboard",
        status_code=303
    )


@app.get(
    "/login",
    response_class=HTMLResponse
)
async def login_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "request": request,
            "error": None
        }
    )


@app.post(
    "/login",
    response_class=HTMLResponse
)
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):

    user = get_user_by_email(
        email
    )

    if (
        not user
        or not verify_password(
            password,
            user["password_hash"]
        )
    ):

        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "request": request,
                "error":
                    "Invalid email or password."
            },
            status_code=401
        )

    request.session["user_id"] = int(
        user["id"]
    )

    return RedirectResponse(
        "/dashboard",
        status_code=303
    )


@app.get("/logout")
async def logout(
    request: Request
):

    request.session.clear()

    return RedirectResponse(
        "/",
        status_code=303
    )


@app.get(
    "/dashboard",
    response_class=HTMLResponse
)
async def dashboard(
    request: Request
):

    user = current_user(request)

    if not user:

        return RedirectResponse(
            "/login",
            status_code=303
        )

    budgets = get_user_budgets(
        int(user["id"])
    )

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,
            "user": user,
            "budgets": budgets
        }
    )


@app.post(
    "/generate",
    response_class=HTMLResponse
)
async def generate_budget(
    request: Request,
    monthly_income: float = Form(...),
    rent: float = Form(0),
    food: float = Form(0),
    transport: float = Form(0),
    utilities: float = Form(0),
    education: float = Form(0),
    healthcare: float = Form(0),
    entertainment: float = Form(0),
    other: float = Form(0),
    savings_goal: float = Form(0)
):

    user = current_user(request)

    if not user:

        return RedirectResponse(
            "/login",
            status_code=303
        )

    data = {
        "monthly_income":
            monthly_income,
        "rent":
            rent,
        "food":
            food,
        "transport":
            transport,
        "utilities":
            utilities,
        "education":
            education,
        "healthcare":
            healthcare,
        "entertainment":
            entertainment,
        "other":
            other,
        "savings_goal":
            savings_goal
    }

    if (
        monthly_income <= 0
        or any(
            value < 0
            for value in data.values()
        )
    ):

        return HTMLResponse(
            "<h2>Invalid budget values.</h2>",
            status_code=400
        )

    recommendation = (
        generate_budget_recommendation(
            data,
            user["name"]
        )
    )

    budget_id = save_budget(
        int(user["id"]),
        data,
        recommendation
    )

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "request": request,
            "user": user,
            "recommendation":
                recommendation,
            "budget_id":
                budget_id,
            "data":
                data
        }
    )


@app.get("/api/health")
async def health():

    return {
        "status": "running",
        "application":
            "PocketSmart AI"
    }


@app.get("/api/gemini-status")
async def gemini_status():

    success, message = (
        validate_gemini_connection()
    )

    return {
        "success": success,
        "message": message
    }


@app.post("/api/recommend")
async def api_recommend(
    data: RecommendationRequest
):

    recommendation = (
        generate_budget_recommendation(
            data.model_dump(
                exclude={"user_name"}
            ),
            data.user_name
        )
    )

    return {
        "success": True,
        "recommendation":
            recommendation
    }


@app.post("/api/budget")
async def api_budget(
    data: BudgetRequest
):

    recommendation = (
        generate_budget_recommendation(
            data.model_dump(),
            "API User"
        )
    )

    return {
        "success": True,
        "recommendation":
            recommendation
    }


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

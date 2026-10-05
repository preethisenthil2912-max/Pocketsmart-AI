from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: str = Field(min_length=5, max_length=150)
    password: str = Field(min_length=6, max_length=128)


class LoginRequest(BaseModel):
    email: str
    password: str


class BudgetRequest(BaseModel):
    monthly_income: float = Field(gt=0)
    rent: float = Field(ge=0)
    food: float = Field(ge=0)
    transport: float = Field(ge=0)
    utilities: float = Field(ge=0)
    education: float = Field(ge=0)
    healthcare: float = Field(ge=0)
    entertainment: float = Field(ge=0)
    other: float = Field(ge=0)
    savings_goal: float = Field(ge=0)


class RecommendationRequest(BudgetRequest):
    user_name: str = "User"

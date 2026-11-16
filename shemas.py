'''Pydantic модели'''
from typing import Annotated
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, StringConstraints, Field


class CategoryCreate(BaseModel):
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)]


class CategoryRename(BaseModel):
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)]


class Category(BaseModel):         
    id: int
    name: str


class Expense(BaseModel):
    id: int
    amount: Annotated[Decimal, Field(gt=0, decimal_places=2)]
    description: str | None = None
    category_id: int
    spent_at: date
    created_at: datetime
    updated_at: datetime | None = None


class CreateExpense(BaseModel):
    amount: Annotated[Decimal, Field(gt=0, decimal_places=2)]
    description: str | None = None
    category_id: int
    spent_at: date


class PatchExpense(BaseModel):
    amount: Annotated[Decimal, Field(gt=0, decimal_places=2)] = None
    description: str | None = None
    category_id: int = None
    spent_at: date = None

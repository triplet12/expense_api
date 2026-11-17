'''Pydantic модели'''
from typing import Annotated, Self
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, StringConstraints, Field, model_validator


def validate_date_range(from_date: date, to_date: date) -> None:
    if from_date > to_date:
        raise ValueError('Некорректная дата: from больше, чем to')


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


class QueryFilters(BaseModel):
    limit: int = Field(50, gt=0, le=100)
    from_date: date | None = Field(None, alias='from')
    to_date: date | None = Field(None, alias='to')
    category_id: int | None = None
    offset: int = Field(0, ge=0)

    @model_validator(mode='after')
    def check_date(self) -> Self:
        if self.from_date and self.to_date:
            validate_date_range(self.from_date, self.to_date)
        return self


class ExpensesPage(BaseModel):
    items: list[Expense]
    total: int
    limit: int
    offset: int


class ReportFilter(BaseModel):
    from_date: date = Field(alias="from")
    to_date: date = Field(alias="to")
    @model_validator(mode='after')
    def check_date(self) -> Self:
        validate_date_range(self.from_date, self.to_date)
        return self



class ByCategory(BaseModel):
    category_id: int
    name: str
    total: Annotated[Decimal, Field(gt=0, decimal_places=2)]
    count: int


class ReportPage(BaseModel):
    from_date: date = Field(serialization_alias="from")
    to_date: date = Field(serialization_alias="to")
    total: Annotated[Decimal, Field(decimal_places=2)]
    count: int
    by_category: list[ByCategory]
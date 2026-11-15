from itertools import count
from typing import Annotated
from datetime import date, datetime
from decimal import Decimal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, StringConstraints, Field


app = FastAPI()


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
    description: str = None
    category_id: int = None
    spent_at: date = None


categories: dict[int, Category] = {}  
expenses: dict[int, Expense] = {}
ids = count(1)      
id_expense = count(1)                  


def is_category_exist(id: int):
    if not categories.get(id):
        raise HTTPException(404, 'Категории не существует') 


def is_expense_exist(id: int):
    if id not in expenses:
        raise HTTPException(404, detail="Тарты с таким ID нет")


@app.post("/categories", status_code=201)
async def create_category(data: CategoryCreate) -> Category:
    name = data.name.capitalize()
    if any(c.name == name for c in categories.values()):
        raise HTTPException(409, detail='Категория с таким именем уже есть')
    category = Category(id=next(ids), name=name)
    categories[category.id] = category
    return category


@app.get("/categories")
async def list_categories() -> list[Category]:
    return list(categories.values())


@app.get("/categories/{category_id}")
async def get_category(category_id: int) -> Category:
    category = categories.get(category_id)
    is_category_exist(category_id)
    return category


@app.patch("/categories/{category_id}")
async def rename_category(category_id: int, data: CategoryRename) -> Category:
    is_category_exist(category_id)
    name = data.name.capitalize()
    if any(c.name == name for c in categories.values()):
        raise HTTPException(409, 'Имя занято или использовано повторно')
    category = Category(id=category_id, name=name)
    categories[category_id] = category
    return category


@app.delete("/categories/{category_id}", status_code=204)
async def del_category(category_id: int) -> None:
    is_category_exist(category_id)
    del categories[category_id]


@app.post("/expenses", status_code=201)
async def add_expense(data: CreateExpense) -> Expense:  
    if data.category_id not in categories:
        raise HTTPException(422, detail="Такой категории нет")
    expense = Expense(id=next(id_expense), created_at=datetime.now(), **data.model_dump())
    expenses[expense.id] = expense
    return expense


@app.get('/expenses')
async def show_expenses() -> list[Expense]:
    return list(expenses.values())


@app.get("/expenses/{expense_id}")
async def show_expense_by_id(expense_id: int) -> Expense:
    is_expense_exist(expense_id)
    return expenses[expense_id]


@app.delete("/expenses/{expense_id}", status_code=204)
async def del_expense(expense_id: int) -> None:
    is_expense_exist(expense_id)
    del expenses[expense_id]


@app.patch("/expenses/{expense_id}")
async def update_expense_by_id(expense_id: int, expense: PatchExpense) -> Expense:
    is_expense_exist(expense_id)
    update_expense = expense.model_dump(exclude_unset=True)
    updated_expense = expenses[expense_id].model_copy(update=update_expense)
    if updated_expense.category_id not in categories:
        raise HTTPException(404, detail="Такой категории нет")
    updated_expense.updated_at = datetime.now()
    expenses[expense_id] = updated_expense
    return updated_expense


@app.get("/health")
async def alive():
    return {"status": "ok"}


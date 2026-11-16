from datetime import datetime

from fastapi import APIRouter, HTTPException

from ..shemas import Expense, PatchExpense, CreateExpense
from ..storage import expenses, id_expense, categories


router = APIRouter(prefix="/expenses", tags=["expenses"])


def is_expense_exist(id: int):
    if id not in expenses:
        raise HTTPException(404, detail="Траты с таким ID нет")


@router.post("/", status_code=201)
async def add_expense(data: CreateExpense) -> Expense:  
    if data.category_id not in categories:
        raise HTTPException(422, detail="Такой категории нет")
    expense = Expense(id=next(id_expense), created_at=datetime.now(), **data.model_dump())
    expenses[expense.id] = expense
    return expense


@router.get('/')
async def show_expenses() -> list[Expense]:
    return list(expenses.values())


@router.get("/{expense_id}")
async def show_expense_by_id(expense_id: int) -> Expense:
    is_expense_exist(expense_id)
    return expenses[expense_id]


@router.delete("/{expense_id}", status_code=204)
async def del_expense(expense_id: int) -> None:
    is_expense_exist(expense_id)
    del expenses[expense_id]


@router.patch("/{expense_id}")
async def update_expense_by_id(expense_id: int, expense: PatchExpense) -> Expense:
    is_expense_exist(expense_id)
    update_expense = expense.model_dump(exclude_unset=True)
    updated_expense = expenses[expense_id].model_copy(update=update_expense)
    if updated_expense.category_id not in categories:
        raise HTTPException(422, detail="Такой категории нет")
    updated_expense.updated_at = datetime.now()
    expenses[expense_id] = updated_expense
    return updated_expense
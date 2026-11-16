from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

from ..schemas import Expense, PatchExpense, CreateExpense
from ..schemas import QueryFilters, ExpensesPage
from ..storage import expenses, id_expense, categories


router = APIRouter(prefix="/expenses", tags=["expenses"])


def is_expense_exist(id: int):
    if id not in expenses:
        raise HTTPException(404, detail="Траты с таким ID нет")


@router.post("", status_code=201)
async def add_expense(data: CreateExpense) -> Expense:  
    if data.category_id not in categories:
        raise HTTPException(422, detail="Такой категории нет")
    expense = Expense(id=next(id_expense), created_at=datetime.now(), **data.model_dump())
    expenses[expense.id] = expense
    return expense


@router.get('') 
async def show_expenses(filter_query: Annotated[QueryFilters, Query()]) -> ExpensesPage:
    items = list(expenses.values())
    if filter_query.from_date is not None:
        items = [x for x in items if x.spent_at >= filter_query.from_date]
    if filter_query.to_date is not None:
        items = [x for x in items if x.spent_at <= filter_query.to_date]
    if filter_query.category_id is not None:
        items = [x for x in items if x.category_id == filter_query.category_id]
    items = sorted(items, key=lambda x: (x.spent_at, x.id), reverse=True)
    total = len(items)
    items = items[filter_query.offset:filter_query.offset + filter_query.limit]
    return ExpensesPage(items=items,
                        limit = filter_query.limit,
                        total=total,
                        offset=filter_query.offset,
                        )



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
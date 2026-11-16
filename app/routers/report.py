from datetime import date

from fastapi import APIRouter, Query
from typing import Annotated

from ..schemas import ByCategory, ReportFilter, ReportPage, Category
from ..storage import categories, expenses

router = APIRouter(prefix="/report", tags=["report"])

def calc_expense(id: int, from_date: date, to_date: date) -> tuple:
    total, count = 0, 0
    for expense in expenses.values():
        if (from_date <= expense.spent_at <= to_date) and (expense.category_id == id):
            total += expense.amount
            count += 1
    return total, count


@router.get("")
async def show_report(filter: Annotated[ReportFilter, Query()]) -> ReportPage:
    by_category = []
    total_count = 0
    for category in categories.values():
        total, count = calc_expense(category.id, filter.from_date, filter.to_date)
        if count > 0:
            by_category.append(ByCategory(category_id=category.id, name = category.name,
                                        total=total, count=count))
            total_count += total
        
    return ReportPage(from_date=filter.from_date, to_date=filter.to_date,
                      count=total_count, by_category=by_category)

'''Словари и счетчики для хранения информации'''
from itertools import count

from .schemas import Category
from .schemas import Expense


categories: dict[int, Category] = {}  
expenses: dict[int, Expense] = {}
ids = count(1)      
id_expense = count(1)              
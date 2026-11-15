from itertools import count
from typing import Annotated

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, StringConstraints

app = FastAPI()


class CategoryCreate(BaseModel):
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)]


class CategoryRename(BaseModel):
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)]


class Category(BaseModel):         
    id: int
    name: str


categories: dict[int, Category] = {}  
used_names = []
ids = count(1)                        


def is_category_exist(id: int):
    if not categories.get(id):
        raise HTTPException(404, 'Категории не существует') 


@app.post("/categories", status_code=201)
async def create_category(data: CategoryCreate) -> Category:
    if data.name.capitalize() in used_names:
        raise HTTPException(409, detail='Категория с таким именем уже есть')
    used_names.append(data.name.capitalize())
    category = Category(id=next(ids), name=data.name.capitalize())
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
    if data.name.capitalize() in used_names:
        raise HTTPException(409, 'Имя занято или использовано повторно')
    used_names.remove(categories[category_id].name)
    category = Category(id=category_id, name=data.name)
    categories[category_id] = category
    used_names.append(data.name.capitalize())
    return category


@app.delete("/categories/{id}", status_code=204)
async def del_category(id: int) -> None:
    is_category_exist(id)
    used_names.remove(categories[id].name)
    del categories[id]


@app.get("/health")
async def alive():
    return {"status": "ok"}
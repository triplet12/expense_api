from itertools import count

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class CategoryCreate(BaseModel):
    name: str = Field(max_length=50)


class CategoryRename(BaseModel):
    name: str = Field(max_length=50)


class Category(BaseModel):         
    id: int
    name: str


categories: dict[int, Category] = {}  
ids = count(1)                        


@app.post("/categories")
async def create_category(data: CategoryCreate) -> Category:
    category = Category(id=next(ids), name=data.name)
    categories[category.id] = category
    return category


@app.get("/categories")
async def list_categories() -> list[Category]:
    return list(categories.values())


@app.get("/categories/{category_id}")
async def category_id(category_id: int) -> Category:
    category = categories.get(category_id)
    return category


@app.patch("/categories/{category_id}")
async def rename_category(category_id: int, data: CategoryRename) -> Category:
    if categories.get(category_id):
        category = Category(id=category_id, name=data.name)
        categories[category_id] = category
    return category


@app.get("/health")
async def alive():
    return {"satus": "ok"}
from fastapi import APIRouter, HTTPException

from ..shemas import Category, CategoryCreate, CategoryRename
from ..storage import categories, ids


router = APIRouter(prefix="/categories", tags=["categories"])


def is_category_exist(id: int):
    if not categories.get(id):
        raise HTTPException(404, 'Категории не существует') 


@router.post("/", status_code=201)
async def create_category(data: CategoryCreate) -> Category:
    name = data.name.capitalize()
    if any(c.name == name for c in categories.values()):
        raise HTTPException(409, detail='Категория с таким именем уже есть')
    category = Category(id=next(ids), name=name)
    categories[category.id] = category
    return category


@router.get("/")
async def list_categories() -> list[Category]:
    return list(categories.values())


@router.get("/{category_id}")
async def get_category(category_id: int) -> Category:
    category = categories.get(category_id)
    is_category_exist(category_id)
    return category


@router.patch("/{category_id}")
async def rename_category(category_id: int, data: CategoryRename) -> Category:
    is_category_exist(category_id)
    name = data.name.capitalize()
    if any(c.name == name for c in categories.values()):
        raise HTTPException(409, 'Имя занято или использовано повторно')
    category = Category(id=category_id, name=name)
    categories[category_id] = category
    return category


@router.delete("/{category_id}", status_code=204)
async def del_category(category_id: int) -> None:
    is_category_exist(category_id)
    del categories[category_id]
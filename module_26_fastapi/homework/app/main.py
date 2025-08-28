from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.models import Base
from app.schemas import RecipeCreate, Recipe, RecipeList
from app.database import get_db, engine
from app.crud import get_recipes, get_recipe, create_recipe

app = FastAPI(
    title="Кулинарная книга API",
    description="API для управления рецептами кулинарной книги",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "Добро пожаловать в кулинарную книгу API"}

@app.get("/recipes/", response_model=List[RecipeList],
         summary="Получить список рецептов",
         description="Возвращает список всех рецептов, отсортированных по популярности (количеству просмотров) и времени приготовления")
async def read_recipes(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    recipes = await get_recipes(db, skip=skip, limit=limit)
    return recipes

@app.get("/recipes/{recipe_id}", response_model=Recipe,
         summary="Получить детальную информацию о рецепте",
         description="Возвращает полную информацию о рецепте, включая ингредиенты и описание. Увеличивает счетчик просмотров.")
async def read_recipe(recipe_id: int, db: AsyncSession = Depends(get_db)):
    db_recipe = await get_recipe(db, recipe_id=recipe_id)
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Рецепт не найден")
    return db_recipe

@app.post("/recipes/", response_model=Recipe,
          summary="Создать новый рецепт",
          description="Добавляет новый рецепт в кулинарную книгу")
async def create_new_recipe(recipe: RecipeCreate, db: AsyncSession = Depends(get_db)):
    return await create_recipe(db, recipe.model_dump())
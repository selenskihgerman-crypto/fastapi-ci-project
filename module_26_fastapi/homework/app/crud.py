from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Recipe

async def get_recipes(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Recipe)
        .order_by(Recipe.views.desc(), Recipe.cooking_time.asc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def get_recipe(db: AsyncSession, recipe_id: int):
    result = await db.execute(
        select(Recipe).where(Recipe.id == recipe_id)
    )
    recipe = result.scalars().first()
    if recipe:
        recipe.views += 1
        await db.commit()
        await db.refresh(recipe)
    return recipe

async def create_recipe(db: AsyncSession, recipe: dict):
    db_recipe = Recipe(**recipe)
    db.add(db_recipe)
    await db.commit()
    await db.refresh(db_recipe)
    return db_recipe
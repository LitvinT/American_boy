from aiogram import Router

from .start import user_start_router
from .category import user_category_router

user_router = Router(name='users')
user_router.include_router(router=user_start_router)
user_router.include_router(router=user_category_router)

__all__: list[str] = [
    'user_router'
]

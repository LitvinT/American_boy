from aiogram import Router

from .start import user_start_router
from .formilize import user_fromilize_router
from .admin import user_admin_router
from .password import user_password_router

user_router = Router(name='users')
user_router.include_router(router=user_start_router)
user_router.include_router(router=user_fromilize_router)
user_router.include_router(router=user_admin_router)
user_router.include_router(router=user_password_router)


__all__: list[str] = [
    'user_router',
]

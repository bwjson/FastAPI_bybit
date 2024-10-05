from fastapi_users.authentication import CookieTransport

cookie_transport = CookieTransport(cookie_max_age=3600)

from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from fastapi_users import FastAPIUsers
from .models import User
from .manager import get_user_manager
from fastapi import Depends, HTTPException, status

from src.auth.models import User
from src.config import SECRET

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=SECRET, 
        lifetime_seconds=3600,
    )

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
current_super_user = fastapi_users.current_user(active=True, superuser=True)

async def is_authenticated(user: User = Depends(current_user)):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    return user

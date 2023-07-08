from typing import Any, Generator, Dict
from fastapi import Depends, HTTPException

# from .security import oauth2_scheme, get_public_key, decode_jwt_token
from app.database.config import SessionLocal


def get_db() -> Generator:
    with SessionLocal() as session:
        yield session


# async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
#     public_key = get_public_key()
#     return decode_jwt_token(token, public_key)
#
#
# async def is_admin(token: str = Depends(oauth2_scheme)) -> Dict:
#     user = await get_current_user(token)
#     if "administrator" not in user["realm_access"]["roles"]:
#         raise HTTPException(401)
#     return user

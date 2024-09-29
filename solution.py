from typing import Annotated
from fastapi import APIRouter, HTTPException, Response, status, Request

router = APIRouter()

@router.post(path="/logout", status_code=status.HTTP_200_OK)
async def logout_user(response: Response, request: ) -> None:
    """
    Logs a user out of their account
    """
    try:
        # do
        pass
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username or Password is incorrect for customer") from e

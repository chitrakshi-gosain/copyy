from enum import Enum
from datetime import timedelta
from typing import List, Literal, Optional
from pydantic import BaseModel, AwareDatetime

class LoginRequest(BaseModel):
    email: str
    password: str
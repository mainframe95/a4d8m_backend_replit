
from fastapi import HTTPException



class CodeExpiredException(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Code expiré")
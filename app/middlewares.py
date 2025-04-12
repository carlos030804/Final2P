from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
import jwt

SECRET_KEY = "secretkey"
ALGORITHM = "HS256"

class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        credentials = await super().__call__(request)
        try:
            payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(403, "Token expirado")
        except jwt.InvalidTokenError:
            raise HTTPException(403, "Token inválido")
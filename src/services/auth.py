from fastapi_jwt import JwtAccessBearerCookie, JwtRefreshBearer, JwtAuthorizationCredentials
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends, Security
from passlib.context import CryptContext
from datetime import timedelta, datetime
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.repository import users as repository_users
from src.conf.config import config

class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = config.secret_key
    ALGORITHM = config.algorithm

    # Read access token from bearer header and cookie (bearer priority)
    access_security = JwtAccessBearerCookie(
        secret_key=SECRET_KEY,
        auto_error=False,
        access_expires_delta=timedelta(hours=1)  # change access token validation timedelta
    )
    # Read refresh token from bearer header only
    refresh_security = JwtRefreshBearer(
        secret_key=SECRET_KEY,
        auto_error=True  # automatically raise HTTPException: HTTP_401_UNAUTHORIZED
    )

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, password: str):
        return cls.pwd_context.hash(password)

    @classmethod
    def get_jti(cls, token: str):
        token = jwt.decode(token, cls.SECRET_KEY, jwt.ALGORITHMS.HS256)
        return token.get("jti")

    def create_email_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire})
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token

    async def get_email_from_token(self, token: str):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email = payload["sub"]
            return email
        except JWTError as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Invalid token for email verification")

async def get_current_user(credentials: JwtAuthorizationCredentials = Security(Auth.access_security),
                           db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not credentials:
        raise credentials_exception

    user = await repository_users.get_user_by_email(credentials["email"], db)
    if user is None:
        raise credentials_exception
    return user


auth_service = Auth()
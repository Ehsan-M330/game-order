from datetime import datetime, timedelta, timezone
from app.auth.dependencies import SECRET_KEY, ALGORITHM
from app import schemas
import jwt

def create_access_token(data:dict, expires_delta: timedelta | None = None):
    to_encode = {'sub':data.user_name , 'role':str(data.role), 'id':data.id}
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import Depends, FastAPI, Response, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import schema, database, models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#SECRET_KEY
#ALGORITHM
#expiration Time

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()  #creates a copy of the data i.e payload
    # expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token : str, credentials_exception):
    try:
         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
         id: str = payload.get("user_id")

         if id is None:
             raise credentials_exception
        #  token_data = schema.TokenData(id=id)   this is throwing error as pydantic_core._pydantic_core.ValidationError: 1 validation error for TokenData id  Input should be a valid string [type=string_type, input_value=10, input_type=int]
 
         token_data = schema.TokenData(id=str(id))

    except JWTError:
        raise credentials_exception   
    
    return token_data # token_data is id

def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail = f"Could not validate credentails", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)   
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user   
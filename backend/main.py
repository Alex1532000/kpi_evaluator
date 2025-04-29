from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import jwt
from datetime import datetime, timedelta

app = FastAPI(title="KPI Evaluator API")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración JWT
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Datos de ejemplo
USERS = {
    "admin": {
        "username": "admin",
        "password": "admin2024",
        "role": "super_admin",
        "name": "Administrador"
    },
    "cesar": {
        "username": "cesar",
        "password": "cesar2024",
        "role": "admin",
        "name": "César"
    },
    "lucia": {
        "username": "lucia",
        "password": "lucia2024",
        "role": "admin",
        "name": "Lucía"
    }
}

class Token(BaseModel):
    access_token: str
    token_type: str
    user_role: str
    user_name: str

class UserLogin(BaseModel):
    username: str
    password: str
    remember_me: Optional[bool] = False

@app.post("/api/login")
async def login(user_data: UserLogin):
    if user_data.username not in USERS or USERS[user_data.username]["password"] != user_data.password:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    
    user = USERS[user_data.username]
    access_token = create_access_token({"sub": user_data.username})
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user_role=user["role"],
        user_name=user["name"]
    )

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.get("/")
async def root():
    return {"message": "KPI Evaluator API is running"}

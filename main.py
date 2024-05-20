from fastapi import FastAPI, status, Form, HTTPException, Path, Query, Body, Depends
from typing import Annotated, Union
from datetime import datetime, time, timedelta
from uuid import UUID

from enums import StoreList
from models import Product, Diabetes, DiabetesExample, Item, User, UserManager
from fastapi.middleware.cors import CORSMiddleware
import pickle
import numpy as np
import warnings
from sklearn.exceptions import InconsistentVersionWarning
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer

warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

app = FastAPI()

data_dict = {1: "Divakar", 2: "John", 3: "Shiv"}

# Default Route - Base url - 
@app.get("/")
async def root():
    return {"message": "Welcome to Fast API tutorial - 20th may"}

@app.get("/user")
async def get_users():
    return data_dict
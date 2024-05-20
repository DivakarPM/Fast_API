from fastapi import FastAPI, status, Form, HTTPException, Path, Query, Body, Depends
from typing import Annotated, Union
from datetime import datetime, time, timedelta
from uuid import UUID
from fastapi.middleware.cors import CORSMiddleware

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)

data_dict = {1: "Divakar", 2: "John", 3: "Shiv"}

# Default Route - Base url - 
@app.get("/")
async def root():
    return {"message": "Welcome to Fast API tutorial - 20th may"}

@app.get("/user")
async def get_users():
    return data_dict

@app.get("/user/{user_id}", response_model=User)
async def get_user_details(user_id: int):
    user_manager = UserManager()
    user = user_manager.get_user(user_id)
    if user:
        return user
    else:
        return {"error": "User not found"}

@app.get("/user/{user_id}")
async def get_user(user_id : int): 
    #Type Safety : Automatically taken care by the Fast API  
    # Check if item_id exists in the dictionary
    if user_id in data_dict.keys():
        return {"item_id": user_id, "value": data_dict[user_id]}
    else:       
        return {"error message" : "No value for this selection"}
        
#---------------  Query Parameter ------------

#Optional Parameter
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

#Multiple Optional Paramters
@app.get("/item_mul/{item_id}")
async def read_item_multiple(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
    
@app.get("/items/{itemid}")
def read_items(itemid: int, q: str):
    return {"item_id": itemid, "q": q}
    
@app.get("/user/{user_id}/item/{item_id}")
async def get_user_items(user_id : int, item_id : int): 
    return {"user_name" : data_dict[user_id], "item_id" : item_id}

@app.get("/item_quantity/{item}")
async def check_item_quantity(item : StoreList):
    item_dict = {StoreList.Milk : 10, StoreList.Bread : 5, 
                 StoreList.Coke : 5, StoreList.Ice_Cream : 12}

    return {"quantity" : item_dict[item]}
    
# Request Body Example
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict
    
 
#http://127.0.0.1:8000/items/1/?item-query=fkdnkfdk 
@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="item_id")],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
   
   
# Query Parameters and String Validations¶
@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
    
    
#Path Variables
@app.post("/item")
async def add_product(item : Product):
    return {"message" : item.name  +" is added to DB"}
    

@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: Annotated[datetime | None, Body()] = None,
    end_datetime: Annotated[datetime | None, Body()] = None,
    repeat_at: Annotated[time | None, Body()] = None,
    process_after: Annotated[timedelta | None, Body()] = None,
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
    }    


@app.post("/add")
async def create_product(item : Product):
    item_dict = item.dict()
    if item.tax:
        total_price = item.price + item.tax
        item_dict.update({"total_price" : total_price})
    return item_dict

@app.put("/update/{item_id}")
async def update_item(item_id : int, item : Product):
    result = {"item_id" : item_id, **item.dict()}
    return result

@app.post("/add_item")
async def add_item(item : StoreList, product : Product):
    return {item,  product.dict()}

@app.delete("/delete/{item_id}", status_code=204)
async def delete_product(item_id : int):
    # No response would be returned here. 
    return item_id

@app.delete("/delete1/{item_id}", status_code=status.HTTP_303_SEE_OTHER)
async def delete_product(item_id : int):
    # No response would be returned here. 
    return item_id

def read_pickle_file():
    return pickle.load(open('model.pkl', 'rb'))

def convert_to_numpy(diabetes_instance: Diabetes):
    # Convert the class instance to a NumPy array
    return np.array([
        diabetes_instance.Pregnancies, diabetes_instance.Glucose,
        diabetes_instance.BloodPressure, diabetes_instance.SkinThickness,
        diabetes_instance.Insulin, diabetes_instance.BMI,
        diabetes_instance.DiabetesPedigreeFunction, diabetes_instance.Age
    ], dtype=float).reshape(1, -1)   
    

@app.post("/predict")
async def predict_value(diabetes_instance : DiabetesExample):
    numpy_data = convert_to_numpy(diabetes_instance)
    model = read_pickle_file()    
    prediction  = model.predict(np.array(numpy_data).reshape(1, -1))
    result_message = "Diabetes is present" if prediction[0] == 1 else "No diabetes"    
    return {"prediction": int(prediction[0]), "result_message": result_message}
    
    


@app.post("/predict")
async def predict_value(diabetes_instance: DiabetesExample):
    try:
        numpy_data = convert_to_numpy(diabetes_instance)
        model = read_pickle_file()    
        prediction = model.predict(np.array(numpy_data).reshape(1, -1))
        
        result_message = "Diabetes is present" if prediction[0] == 1 else "No diabetes"
        
        return {"prediction": int(prediction[0]), "result_message": result_message}
    except Exception as e:
        # Log the exception or handle it accordingly
        raise HTTPException(status_code=500, detail="Internal Server Error")

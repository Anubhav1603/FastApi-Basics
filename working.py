from fastapi import FastAPI, Path, Query, HTTPException
from typing import Optional
from pydantic import BaseModel


app = FastAPI()

inventory = {}

class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None

class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None

@app.get("/")
def home():
    return {"Data" : "Test"}

@app.get("/about")
def about():
    return {"About": "Nothing to say"}

@app.get("/get-item/{item_id}", status_code=200)
def get_item(item_id: int = Path(None, description='The id of the item you want to view', gt = 0)):
    return inventory[item_id]

@app.get("/get-by-name")
def get_item(name: str = Query(None, description='Name of the item.')):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    raise HTTPException(status_code=404, detail="Item id not found")

@app.post("/create-item/{item_id}",status_code=200)
def create_item(item_id: int, item: Item):
    """Creates items at inventory dict"""

    if item_id in inventory:
        raise HTTPException(status_code=404, detail="Item id already exist",)
    
    inventory[item_id] = item
    return inventory[item_id]

@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    """Updates items at inventory dict"""

    if item_id not in inventory:
        return {"Error": "Item ID does not exists"}

    if item.name != None:
        inventory[item_id].name = item.name
    if item.brand != None:
        inventory[item_id].brand = item.brand
    if item.price != None:
        inventory[item_id].price = item.price
    return inventory[item_id]

@app.delete("/delete-item")

def delete_item(item_id: int = Query(..., description = 'The ID of the item you want to delete', gt =0 )):
    if item_id not in inventory:
        return {"Error": "Item ID does not exists"}
    
    del inventory[item_id]
    return {"Success" : f"item of id {item_id} has been deleted!"}

#pip install python-multipart
# @app.post("/login/")
# async def login(username: str = Form(...), password: str = Form(...)):
#     return {"username": username}
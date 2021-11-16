from typing import Optional, List
from enum import Enum

from pydantic import BaseModel

from fastapi import FastAPI, Query, Path

app = FastAPI()

class ItemName(str, Enum):
    alexnet = 'alexnet'
    resnet = 'resnet'
    lenet = 'lenet'

@app.get("/")
def read_root():
    return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}

@app.get("/item_name/{item_name}")
def get_items(item_name: ItemName):
    if item_name == ItemName.alexnet:
        return {"model_name": item_name, "message": "Deep Learning FTW!"}

    if item_name.value == "lenet":
        return {"model_name": item_name, "message": "LeCNN all the images"}

    return {"model_name": item_name, "message": "Have some residuals"}

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
def read_item(skip: int = 0, limit: int = 10):

    return fake_items_db[skip : skip + limit]


@app.get("/itemsList/")
def read_items2(q: Optional[List[str]] = Query(None)):

    query_items = {"q": q}
    return query_items


@app.get("/title/")
def title(

    q: Optional[str] = Query(None, title="Query string", min_length=3)

):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

class Item(BaseModel): #body를 위해 선언
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None



@app.put("/items/{item_id}")
def create_item(item_id: int, item: Item):

    return {"item_id": item_id, **item.dict()}


@app.get("/param")
def param(param: int):
    return param


@app.get("/path/{item_id}")
def path(

    *, item_id: int = Path(..., title="The ID of the item to get"), q: str

):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
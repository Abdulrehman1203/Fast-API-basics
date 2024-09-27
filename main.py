# from fastapi import FastAPI
#
# app = FastAPI()
#
# """ Defining Routes Using HTTP Methods """
#
#
# @app.get("/get/items/")
# def get_items():
#     return {"message": "List of items"}
#
#
# @app.post("/items/")
# def create_item(item: dict):
#     return {"message": f"Item {item} created"}
#
#
# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: dict):
#     return {"message": f"Item {item_id} updated with {item}"}
#
#
# @app.delete("/items/{item_id}")
# def delete_item(item_id: int):
#     return {"message": f"Item {item_id} deleted"}
#
#
# """ Path parameter """
#
#
# @app.get("/items/{item_id}")
# def read_item(item_id: int):
#     return {"item_id": item_id}
#
#
# """ Query parameter """
#
#
# @app.get("/items/")
# def read_items(skip: int = 0, limit: int = 10):
#     return {"skip": skip, "limit": limit}
#
#
# """ Combined Path and Query Parameters """
#
#
# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None):
#     if q:
#         return {"item_id": item_id, "q": q}
#     return {"item_id": item_id}

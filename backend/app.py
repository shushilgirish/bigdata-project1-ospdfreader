from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()


class User(BaseModel):
    name: str
    age: int

@app.get("/")
async def root():
    return {"message": "Welcome to the Basic FASTAPI App example!"}

@app.post("/greet/")
async def create_item(user: User):
    if user.age >0 and user.age < 18:
        return {"message": f"Sorry {user.name}, you are too young to use this app."}
    elif user.age >= 18:
        return {"message": f"Welcome {user.name}!, Welcome to the app."}
    else:
        return {"message": "Invalid age."}
    
@app.get("/square/{number}")
async def square_number(number: int):
    return {"number": number, "square": number ** 2}




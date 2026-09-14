import time
from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel 

app = FastAPI(title="Phase 15 - Python APIs")


# ---------- Pydantic Validation  ----------

# Pydantic models define the SHAPE of expected data, and automatically
# validate incoming request bodies against it - if the data doesn't match,
# FastAPI returns a clear error automatically, before your code even runs.
class User(BaseModel):
    name: str
    email: str
    role: str


# ---------- In-Memory Data Store ----------
users = {
    1: {
        "id": 1,
        "name": "Mona",
        "email": "monamobeen@yahoo.com",
        "role": "Engineer",
        "city": "Lahore"
    },
     2: {
         "id": 2,
         "name": "Mobeen", 
         "email": "mobeenmona@yahoo.com",
         "role": "OD & Culture",
         "city": "FSD"
         },
}


# ---------- GET ----------
# Get a user by ID
@app.get("/users/{user_id}")
def get_user(user_id: int):

    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return users[user_id]


# ---------- POST ----------
# Create a new user
@app.post("/users", status_code=201)
def create_user(user: User):

    new_id = len(users) + 1

    users[new_id] = {
        "id": new_id,
        **user.model_dump()
    }

    return users[new_id]


# ---------- PUT ----------
# Completely replace an existing user
@app.put("/users/{user_id}")
def replace_user(user_id: int, user: User):

    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    users[user_id] = {
        "id": user_id,
        **user.model_dump()
    }

    return users[user_id]


# ---------- DELETE ----------
# Delete an existing user
@app.delete("/users/{user_id}")
def delete_user(user_id: int):

    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    deleted_user = users.pop(user_id)

    return {
        "message": "User deleted",
        "user": deleted_user
    }


# ---------- Dependency Injection ----------
def get_current_user():
    return {
        "username": "Monaa"
    }


@app.get("/admin")
def admin(user=Depends(get_current_user)):

    return {
        "message": "Welcome Admin",
        "user": user
    }


# ---------- Middleware ----------

# Middleware runs code BEFORE and AFTER every request, regardless of
# which endpoint was called - useful for logging, timing, or auth checks.
@app.middleware("http")
async def log_requests(request, call_next):

    print("Request:", request.method, request.url)

    response = await call_next(request)

    print("Status:", response.status_code)

    return response


# ---------- Async Endpoint ----------
@app.get("/async")
async def async_endpoint():

    return {
        "message": "Async endpoint"
    }
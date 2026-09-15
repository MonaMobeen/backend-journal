import time
from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel 

app = FastAPI(title="Phase 15 - Python APIs")
"""
HOW TO RUN:
1. Install dependencies (one time):
   pip install fastapi uvicorn --break-system-packages
 
2. Start the server:
   uvicorn main:app --reload
 
3. Open interactive docs:
   http://127.0.0.1:8000/docs
"""
# ---------- Pydantic Validation  ----------

# Pydantic models define the SHAPE of expected data, and automatically
# validate incoming request bodies against it - if the data doesn't match,
# FastAPI returns a clear error automatically, before your code even runs.
class User(BaseModel):
    name: str
    email: str
    role: str
    city: str


class UserUpdate(BaseModel):
    """All fields optional - used for PATCH (partial updates)."""
    name: str | None = None
    email: str | None = None
    role: str | None = None
    city: str | None = None
    
    
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


# ---------- Middleware ----------

# Middleware runs code BEFORE and AFTER every request, regardless of
# which endpoint was called - useful for logging, timing, or auth checks.
@app.middleware("http")
async def log_requests(request, call_next):

    print("Request:", request.method, request.url)

    response = await call_next(request)

    print("Status:", response.status_code)

    return response

# ---------- Dependency Injection ----------
def get_current_user():
    return {"username": "Mona"}
 
 
def verify_user_exists(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return user_id


# ---------- GET (list + query params) ----------
@app.get("/users")
def list_users(role: str | None = None, city: str | None = None, limit: int = 10):
    """
    Query parameter example:
    /users?role=Engineer&city=Lahore&limit=5
    Query params are optional filters passed after the "?" in a URL.
    """
    results = list(users.values())
    if role:
        results = [u for u in results if u["role"] == role]
    if city:
        results = [u for u in results if u["city"] == city]
    return results[:limit]
 
 
# ---------- GET (single user by path param) ----------
@app.get("/users/{user_id}")
def get_user(user_id: int = Depends(verify_user_exists)):
    return users[user_id]
 
 
# ---------- POST ----------
@app.post("/users", status_code=201)
def create_user(user: User):
    new_id = max(users.keys()) + 1
    users[new_id] = {"id": new_id, **user.model_dump()}
    return users[new_id]
 
 
# ---------- PUT (full replace) ----------
@app.put("/users/{user_id}")
def replace_user(user: User, user_id: int = Depends(verify_user_exists)):
    users[user_id] = {"id": user_id, **user.model_dump()}
    return users[user_id]
 
 
# ---------- PATCH (partial update) ----------
@app.patch("/users/{user_id}")
def update_user(user: UserUpdate, user_id: int = Depends(verify_user_exists)):
    stored_user = users[user_id]
    updates = user.model_dump(exclude_unset=True)  # only fields the client actually sent
    stored_user.update(updates)
    return stored_user
 
 
# ---------- DELETE ----------
@app.delete("/users/{user_id}", status_code=200)
def delete_user(user_id: int = Depends(verify_user_exists)):
    deleted_user = users.pop(user_id)
    return {"message": "User deleted", "user": deleted_user}


# ---------- Async Endpoint ----------
@app.get("/async")
async def async_endpoint():

    return {
        "message": "Async endpoint"
    }
    
    
# ---------- Common HTTP Status Codes Reference ----------
# 200 OK              - request succeeded
# 201 Created         - new resource created successfully (POST)
# 204 No Content      - success, but nothing to return (DELETE, if no body)
# 400 Bad Request     - client sent invalid data
# 401 Unauthorized    - authentication required
# 403 Forbidden       - authenticated, but not allowed to do this
# 404 Not Found       - resource doesn't exist
# 500 Internal Server Error - something broke on the server side
 
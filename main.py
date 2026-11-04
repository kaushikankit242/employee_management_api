from fastapi import FastAPI

from APP.routers import auth, employees, departments

app = FastAPI(
    title="Employee Management API",
    description="Employee Management with JWT Authentication",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(employees.router)
app.include_router(departments.router)


@app.get("/")
def home():
    return {"message": "Employee Management API is running"}



from fastapi import Depends

from APP.security import get_current_user


@app.get("/users/me")
def get_user(current_user=Depends(get_current_user)):

    return {
        "message": "Access granted",
        "user": current_user
    }
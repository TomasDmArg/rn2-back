from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import user, todo

app = FastAPI(
    title="Todo API",
    description="A simple Todo API with user authentication",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "users",
            "description": "Operations with users. The **login** logic is also here.",
        },
        {
            "name": "todos",
            "description": "Manage todos. Requires authentication.",
        },
    ]
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user.router, tags=["users"])
app.include_router(todo.router, tags=["todos"])

@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint of the API.
    """
    return {"message": "Welcome to the Todo API"}
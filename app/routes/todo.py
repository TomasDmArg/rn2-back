from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.todo import Todo, TodoCreate, TodoUpdate
from ..crud import todo as todo_crud
from ..auth.jwt_handler import AuthHandler

router = APIRouter()
auth_handler = AuthHandler()

@router.post("/todos/", response_model=Todo)
async def create_todo(
    todo: TodoCreate, 
    db: Session = Depends(get_db), 
    current_user_id: int = Depends(auth_handler.auth_wrapper)
):
    """
    Create a new todo for the authenticated user.
    
    - **title**: The title of the todo
    - **description**: An optional description of the todo
    
    Returns the created todo.
    """
    return todo_crud.create_user_todo(db=db, todo=todo, user_id=current_user_id)

@router.get("/todos/", response_model=List[Todo])
async def read_todos(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user_id: int = Depends(auth_handler.auth_wrapper)
):
    """
    Retrieve todos for the authenticated user.
    
    - **skip**: Number of todos to skip (for pagination)
    - **limit**: Maximum number of todos to return
    
    Returns a list of todos for the authenticated user.
    """
    todos = todo_crud.get_todos(db, skip=skip, limit=limit, user_id=current_user_id)
    return todos

@router.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(
    todo_id: int, 
    todo: TodoUpdate, 
    db: Session = Depends(get_db), 
    current_user_id: int = Depends(auth_handler.auth_wrapper)
):
    """
    Update a specific todo for the authenticated user.
    
    - **todo_id**: The ID of the todo to update
    - **title**: The new title of the todo (optional)
    - **description**: The new description of the todo (optional)
    - **completed**: The new completed status of the todo (optional)
    
    Returns the updated todo.
    """
    db_todo = todo_crud.get_todo(db, todo_id=todo_id)
    if db_todo is None or db_todo.owner_id != current_user_id:
        raise HTTPException(status_code=404, detail="Todo not found or not owned by user")
    return todo_crud.update_todo(db=db, todo=todo, todo_id=todo_id)

@router.delete("/todos/{todo_id}", response_model=Todo)
async def delete_todo(
    todo_id: int, 
    db: Session = Depends(get_db), 
    current_user_id: int = Depends(auth_handler.auth_wrapper)
):
    """
    Delete a specific todo for the authenticated user.
    
    - **todo_id**: The ID of the todo to delete
    
    Returns the deleted todo.
    """
    db_todo = todo_crud.get_todo(db, todo_id=todo_id)
    if db_todo is None or db_todo.owner_id != current_user_id:
        raise HTTPException(status_code=404, detail="Todo not found or not owned by user")
    return todo_crud.delete_todo(db=db, todo_id=todo_id)
from sqlalchemy.orm import Session
from ..models.todo import Todo
from ..schemas.todo import TodoCreate, TodoUpdate
from fastapi import HTTPException, status

def get_todos(db: Session, skip: int = 0, limit: int = 100, user_id: int = None):
    query = db.query(Todo)
    if user_id:
        query = query.filter(Todo.owner_id == user_id)
    return query.offset(skip).limit(limit).all()

def create_user_todo(db: Session, todo: TodoCreate, user_id: int):
    db_todo = Todo(**todo.dict(), owner_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def get_todo(db: Session, todo_id: int, user_id: int):
    todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.owner_id == user_id
    ).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return todo

def update_todo(db: Session, todo_id: int, todo_update: TodoUpdate, user_id: int):
    db_todo = get_todo(db, todo_id=todo_id, user_id=user_id)
    
    # Si solo estamos actualizando completed, manejarlo específicamente
    if len(todo_update.dict(exclude_unset=True)) == 1 and "completed" in todo_update.dict(exclude_unset=True):
        db_todo.completed = todo_update.completed
    else:
        # Para otras actualizaciones, actualizar todos los campos proporcionados
        update_data = todo_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_todo, key, value)
    
    try:
        db.commit()
        db.refresh(db_todo)
        return db_todo
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating todo"
        )

def delete_todo(db: Session, todo_id: int, user_id: int):
    db_todo = get_todo(db, todo_id=todo_id, user_id=user_id)
    try:
        db.delete(db_todo)
        db.commit()
        return db_todo
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting todo"
        )
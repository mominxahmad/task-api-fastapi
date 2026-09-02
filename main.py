from sqlalchemy import create_engine,Column,Integer,String,Boolean
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy.ext.declarative import declarative_base
from typing import Annotated
from fastapi import FastAPI,Depends,HTTPException,Path,Query
from starlette import status
from pydantic import BaseModel, Field

#DB CONFIG
DB_URL = "sqlite:///./tasks.db"
engine = create_engine(DB_URL,connect_args={"check_same_thread":False})
SessionLocal = sessionmaker(engine,autocommit=False,autoflush=False)
Base = declarative_base()


#DB MODELS SETUP
class Tasks(Base):
    __tablename__ = "tasks"
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String,nullable=False)
    done = Column(Boolean,default=False)


#FASTAPI APP
app = FastAPI(title="Tasks To-do List")


#AUTO-CREATE DB
Base.metadata.create_all(bind=engine)


#DEPENDENCY INJECTION CONFIG.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency_injection = Annotated[Session,Depends(get_db)]


#AUTO-INSERTING SAMPLE ROWS IF DB EMPTY
def check_db():  #FastAPI resolves Depends() when it calls path operation so cant use dependency-injection
    db = SessionLocal()  #This func runs at app startup so must create session directly
    try:
        counter = db.query(Tasks).count()
        if counter == 0:
            task1 = Tasks(title="Do grocery")
            task2 = Tasks(title="Wash helmet padding",done=True)
            task3 = Tasks(title="Buy a birthday gift for Ali")
            db.add_all([task1,task2,task3])
            db.commit()
    finally:
        db.close()

check_db()


#REQUEST VALIDATION WITH PYDANTIC
class TaskRequests(BaseModel):
    #id auto-assigned
    title: str = Field(examples=["Task Name"])
    done: bool = Field(default=False)


#===================ENDPOINTS==================================================
@app.get("/")
async def api_root():
    return {"name" : "Task API", "version" : "2.0", "endpoints" : ["/tasks"]}


@app.get("/health")
async def health_check():
    return {"status" : "ok"}


@app.get("/tasks")
async def all_tasks(db: db_dependency_injection):
    return db.query(Tasks).all()


@app.get("/tasks/{id}")
async def task_by_id(db:db_dependency_injection, id: int = Path(gt=0)):
    task_to_return = db.query(Tasks).filter(Tasks.id==id).first()
    if task_to_return is None:
        raise HTTPException(status_code=404, detail={"error": f"Task {id} not found"})
    return task_to_return


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
async def add_new_task(db: db_dependency_injection, task_title: TaskRequests):
    if not task_title.title: raise HTTPException(status_code=400, detail={"error" : "Task Title is Missing/Null"})
    new_task = Tasks(**task_title.model_dump())
    db.add(new_task)
    db.commit()


@app.put("/tasks/{id}",status_code=status.HTTP_200_OK)
async def update_title_by_id(db: db_dependency_injection, updated_task: TaskRequests,id: int = Path(gt=0), ):
    task_to_update = db.query(Tasks).filter(Tasks.id==id).first()
    if not task_to_update: raise HTTPException(status_code=404,detail={"error": "Task {id} not found"})
    if not updated_task.title: raise HTTPException(status_code=400, detail={"error": "Task Title is Missing/Null"})
    task_to_update.title = updated_task.title
    task_to_update.done = updated_task.done
    db.add(task_to_update)
    db.commit()

    return db.query(Tasks).filter(Tasks.id==id).first()


@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_by_id(db:db_dependency_injection, id: int = Path(gt=0)):
    task_to_delete = db.query(Tasks).filter(Tasks.id==id).first()
    if not task_to_delete: raise HTTPException(status_code=404,detail={"error": "Task {id} not found"})
    db.query(Tasks).filter(Tasks.id == id).delete()
    db.commit()

#played around with the db in db-browser using sql queries

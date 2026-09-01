from sqlalchemy import create_engine,Column,Integer,String,Boolean
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy.ext.declarative import declarative_base
from typing import Annotated
from fastapi import FastAPI,Depends,HTTPException,Path,Query
from starlette import status


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


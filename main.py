from fastapi import FastAPI, Body, HTTPException, status


app = FastAPI()


TASKS = [
    {"id" : 1, "title" : "Do grocery", "done" : False},
    {"id" : 2, "title" : "Wash helmet padding", "done" : True},
    {"id" : 3, "title" : "Buy a birthday gift for Ali", "done" : False},
]


@app.get("/")
async def api_root():
    return {"name" : "Task API", "version" : "1.0", "endpoints" : ["/tasks"]}


@app.get("/health")
async def health_check():
    return {"status" : "ok"}


@app.get("/tasks")
async def all_tasks():
    return TASKS


@app.get("/tasks/{id}")
async def task_by_id(id: int):
    tasks_to_return=[]
    for task in TASKS:
        if task["id"]==id:
            tasks_to_return.append(task)
    if not tasks_to_return: raise HTTPException(status_code=404, detail={"error": f"task {id} not found"})
    return tasks_to_return


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
async def add_new_task(task_title: str = Body()):
    if not task_title: raise HTTPException(status_code=400, detail={"error" : "task title is missing/null"})
    TASKS.append({"id": len(TASKS)+1, "title": task_title, "done": False})


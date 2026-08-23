# Task Management CRUD API
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-00a393.svg)
![License](https://img.shields.io/badge/Status-Completed-success.svg)

A lightweight, in-memory RESTful API built to manage a to-do list. I have developed this portfolio project while doing **FastAPI - The Complete Course 2026 (Beginner + Advanced)** on Udemy as practice. 

The API demonstrates foundational backend concepts, including full CRUD operations (Create, Read, Update, Delete)[cite: 1], RESTful path routing, and strict HTTP status code validation.

## Quick Start

To run this API locally, clone the repository and execute the following command in your terminal. *(Note: Requires `uvicorn` and `fastapi` to be installed).*

```bash
uvicorn main:app --reload
```

The server will boot up instantly on `http://localhost:8000`.

---

## API Reference

| HTTP Method | Endpoint | Description | Expected Status Codes |
| --- | --- | --- | --- |
| **GET** | `/` | Returns API metadata. | `200 OK`<br> |
| **GET** | `/health` | Server heartbeat check. | `200 OK`<br> |
| **GET** | `/tasks` | Retrieves all tasks. | `200 OK`<br> |
| **GET** | `/tasks/{id}` | Retrieves a single task. | `200 OK`, `404 Not Found`<br> |
| **POST** | `/tasks` | Creates a new task. | `201 Created`, `400 Bad Request`<br> |
| **PUT** | `/tasks/{id}` | Updates an existing task. | `200 OK`, `400 Bad Request`, `404 Not Found`<br> |
| **DELETE** | `/tasks/{id}` | Deletes a task. | `204 No Content`, `404 Not Found`<br> |

---

## Testing the API

**Example `curl` Request:**

```bash
curl -i http://localhost:8000/

```

**Expected Response:**

```http
HTTP/1.1 200 OK
server: uvicorn
content-length: 56
content-type: application/json

{"name":"Task API","version":"1.0","endpoints":["/tasks"]}

```

---

## Interactive Documentation (Swagger UI)

Because this API is built with FastAPI, OpenAPI interactive documentation is generated automatically.

You can test the full CRUD cycle directly from your browser without using the terminal by navigating to:
**`http://localhost:8000/docs`**
### Screenshots
![Swagger UI Screenshot 1](./assets/img.png) 
![Swagger UI Screenshot 2](./assets/img_1.png)
# Student Management System

A full-stack Student Management System built with **Vue.js 3**, **FastAPI**, and **MySQL**. The application provides complete CRUD functionality for managing student records.

## Tech Stack

### Frontend
- Vue.js 3
- Vite
- Composition API (`<script setup>`)
- Axios

### Backend
- Python
- FastAPI
- SQLAlchemy
- PyMySQL

### Database
- MySQL
- Database: `student_management_system`
- Table: `students`

## Features

- Add new students
- View all students
- View individual student details
- Update student information
- Delete student records
- Active / Inactive student status

## Project Structure

```text
student-management-system/
├── frontend/
│   ├── src/
│   └── package.json
│
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   └── requirements.txt
│
└── README.md
```

## Database

The `students` table contains:

| Column | Description |
|---|---|
| `id` | Primary key, auto-increment |
| `name` | Student name |
| `email` | Unique email |
| `age` | Student age |
| `course` | Course name |
| `phone` | Phone number |
| `address` | Student address |
| `status` | Active / Inactive |
| `created_at` | Creation timestamp |
| `updated_at` | Last update timestamp |

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/students` | Get all students |
| GET | `/students/{id}` | Get student by ID |
| POST | `/students` | Create a student |
| PUT | `/students/{id}` | Update a student |
| DELETE | `/students/{id}` | Delete a student |

## How to Run

### 1. Start the Backend

```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger API Documentation:

```text
http://127.0.0.1:8000/docs
```

### 2. Start the Frontend

Open another terminal:

```powershell
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

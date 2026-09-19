# Student Management System

Full-stack CRUD app — Vue.js 3 (frontend) + FastAPI (backend) + MySQL (database).

## Tech Stack
- Frontend: Vue.js 3 (Vite, Composition API `<script setup>`), Axios
- Backend: Python FastAPI, SQLAlchemy, PyMySQL
- Database: MySQL (`student_management_system` DB, `students` table)

## Folder Structure

student-management-system/
├── backend/
│ ├── venv/ (Python virtual env)
│ ├── .env (DB credentials - not in git)
│ ├── database.py (SQLAlchemy engine + session setup)
│ ├── models.py (Student SQLAlchemy model)
│ ├── schemas.py (Pydantic schemas: Create/Update/Response)
│ ├── main.py (FastAPI app + all 6 endpoints)
│ └── requirements.txt
└── frontend/
├── src/
│ ├── api.js (Axios instance, baseURL http://127.0.0.1:8000)
│ ├── App.vue (Main layout: sidebar + topbar + stats + form + table)
│ ├── components/
│ │ └── Sidebar.vue (Sidebar nav - separate component)
│ └── StudentForm.vue (Add/Edit form - same component, dual mode)
└── package.json


## How to Run

**Backend:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload
```
Runs on http://127.0.0.1:8000 — Docs at http://127.0.0.1:8000/docs

**Frontend:**
```powershell
cd frontend
npm run dev
```
Runs on http://localhost:5173

**Both must run together** (2 separate terminals) for the app to work.

## Database (students table)
Columns: id (PK, auto), name, email (unique), age, course, phone, address,
status (Enum: Active/Inactive, default Active), created_at, updated_at (auto timestamps)

## API Endpoints (all working, tested via Swagger)
| Method | Route | Purpose |
|--------|-------|---------|
| GET | /students | List all |
| GET | /students/{id} | Get one |
| POST | /students | Create |
| PUT | /students/{id} | Update |
| DELETE | /students/{id} | Delete |

## Progress So Far (Phases Completed)
- [x] Phase 1: Project setup (folders, git, .gitignore)
- [x] Phase 2: MySQL database + students table
- [x] Phase 3: FastAPI backend setup + venv
- [x] Phase 4: SQLAlchemy DB connection (database.py)
- [x] Phase 5: models.py + schemas.py
- [x] Phase 6: main.py — full CRUD API (tested in Swagger, working)
- [x] Phase 7: Vue.js frontend setup + Axios installed
- [x] Phase 8: Student list fetch + display (working)
- [x] Phase 9: Add Student form (working, list auto-refreshes)
- [x] Phase 10: Edit + Delete functionality (working)
- [ ] Phase 11: Dashboard-style UI redesign (IN PROGRESS)
  - Sidebar, topbar, stat cards, search, pagination added
  - Currently: extracting Sidebar into its own component
  - App.vue and StudentForm.vue content was reset/cleared — needs re-adding

## Known Issues / Notes
- Sidebar icons/text were misaligned — fixed via flex layout in CSS
- Table was overflowing horizontally — fixed with `.table-wrapper { overflow-x: auto }`
- `v-else` must be on the immediate sibling of matching `v-if` (Vue rule) — caused
  an earlier bug when wrapping the table in a div

## Next Steps
- Finish Sidebar.vue component extraction
- Re-verify full CRUD still works after UI redesign
- (Later, optional) Search/filter polish, validation improvements, styling tweaks
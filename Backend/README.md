# Vidwan Classes FastAPI Backend

Production-ready, high-performance REST API backend for the Vidwan Classes platform.

## Features & Tech Stack

- **Framework**: FastAPI (Python 3.10+)
- **ORM & Database**: SQLAlchemy 2.x, PostgreSQL (psycopg2) / SQLite for local development
- **Validation**: Pydantic v2
- **Database Migrations**: Alembic
- **Authentication**: OAuth2 / JWT Tokens with bcrypt password hashing
- **Services**: SMTP Email Notifications (HTML templates for Admin & Students), Configurable Media Storage Service
- **Testing**: pytest & HTTPX

---

## Folder Architecture

```text
backend/
├── app/
│   ├── api/
│   │   └── routes/         # Endpoint route handlers (courses, faculty, vst, contact, etc.)
│   ├── core/               # Configuration, security (JWT, bcrypt), database engine
│   ├── dependencies/       # FastAPI dependency injection (get_current_admin, DB sessions)
│   ├── models/             # SQLAlchemy DB Models (User, Course, Faculty, Result, Enquiry, etc.)
│   ├── schemas/            # Pydantic Schemas for request & response validation
│   ├── services/           # Reusable services (Email SMTP, Storage, Enquiry handling)
│   └── main.py             # FastAPI entrypoint, CORS & Exception Middleware
├── alembic/                # Schema migration scripts
├── tests/                  # Pytest test suite
├── uploads/                # Local static media storage directory
├── seed.py                 # Automated Database Seeder Script
├── .env.example            # Environment variables template
├── alembic.ini             # Alembic migration configuration
├── requirements.txt        # Production dependencies
└── README.md               # Backend documentation
```

---

## Setup & Running Locally

### 1. Create Virtual Environment & Install Dependencies

```bash
cd backend
python -m venv venv

# On Windows PowerShell:
.\venv\Scripts\Activate.ps1

# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Adjust `.env` parameters:
- `DATABASE_URL`: `sqlite:///./vidwan.db` (for local dev) or `postgresql://user:pass@localhost:5432/vidwan_db` (for production)
- `SECRET_KEY`: Set a strong random secret key.
- `FRONTEND_URL`: Allowed origins for CORS (e.g. `http://localhost:5173,http://127.0.0.1:5500`)

### 3. Initialize Database & Seed Initial Data

```bash
# Run database migrations
alembic upgrade head

# Run seeder script (Creates admin user & default courses/faculty/results)
python seed.py
```

Default Admin Credentials created by `seed.py`:
- **Email**: `admin@vidwanclasses.com`
- **Password**: `Admin@12345`

### 4. Start Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Interactive API documentation available at:
- Swagger Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## API Endpoints Overview (`/api/v1/`)

| Tag | Method | Endpoint | Description |
|---|---|---|---|
| **Health** | GET | `/api/v1/health` | Backend & DB health status |
| **Auth** | POST | `/api/v1/auth/login` | Obtain OAuth2 JWT token |
| **Auth** | GET | `/api/v1/auth/me` | Current authenticated admin profile |
| **Courses** | GET | `/api/v1/courses` | List active courses |
| **Courses** | GET | `/api/v1/courses/{id_or_slug}` | Course details by slug (nurture, qualifier, etc.) |
| **Faculty** | GET | `/api/v1/faculty` | List faculty members |
| **Results** | GET | `/api/v1/results` | List rankers / achievements |
| **Gallery** | GET | `/api/v1/gallery` | Gallery items with `?category=` filter |
| **Testimonials**| GET | `/api/v1/testimonials` | Approved student testimonials |
| **Contact** | POST | `/api/v1/contact` | Submit contact form (DB + SMTP email) |
| **Enquiries** | POST | `/api/v1/enquiries` | Submit hero, callback, demo, application forms |
| **VST** | POST | `/api/v1/vst/register` | Vidwan Scholarship Test registration |
| **Newsletter**| POST | `/api/v1/newsletter/subscribe` | Subscribe email newsletter |
| **Admin** | GET | `/api/v1/admin/dashboard/stats` | Live stats for Admin Dashboard |
| **Admin** | GET | `/api/v1/admin/enquiries` | List & filter enquiries by status |
| **Admin** | PUT | `/api/v1/admin/enquiries/{id}` | Update enquiry status (new, contacted, closed) |

---

## Running Tests

```bash
pytest
```

---

## Production Deployment (Render / Railway)

1. **Host Backend Service**:
   - Create a Web Service on Render or Railway pointing to the `backend/` folder.
   - Build Command: `pip install -r requirements.txt && alembic upgrade head && python seed.py`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

2. **Configure Database**:
   - Provision a PostgreSQL database (e.g. Supabase, Render Postgres, or Railway Postgres).
   - Set `DATABASE_URL` in hosting provider environment variables.

3. **Configure CORS**:
   - Set `FRONTEND_URL="https://vidwanclasses.vercel.app"` in hosting environment.

4. **Connect Vercel Frontend**:
   - Set `VIDWAN_API_URL="https://your-backend-render-app.onrender.com/api/v1"` in Vercel environment settings.

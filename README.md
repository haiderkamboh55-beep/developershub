# DevelopersHub — Full-Stack Agency Platform

A complete full-stack web application built with **Flask + PostgreSQL** (backend) and **Vanilla HTML/CSS/JS** (frontend).

---

## Project Structure

```
developershub/
├── frontend/
│   ├── index.html                  # Home page
│   ├── css/
│   │   ├── style.css               # Main styles
│   │   └── admin.css               # Admin panel styles
│   ├── js/
│   │   └── main.js                 # API helpers + shared logic
│   └── pages/
│       ├── about.html
│       ├── services.html
│       ├── portfolio.html
│       ├── blog.html
│       ├── contact.html
│       ├── booking.html
│       └── admin/
│           ├── login.html
│           ├── dashboard.html
│           ├── services.html
│           ├── portfolio.html
│           ├── blog.html
│           ├── inquiries.html
│           └── bookings.html
└── backend/
    ├── app.py                      # Flask entry point
    ├── config.py                   # Configuration
    ├── db.py                       # Database connection + init
    ├── auth_utils.py               # JWT + password helpers
    ├── seed.py                     # Database seeder
    ├── requirements.txt
    ├── .env.example
    └── routes/
        ├── auth.py
        ├── services.py
        ├── portfolio.py
        ├── blog.py
        ├── contact.py
        └── booking.py
```

---

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- PostgreSQL (running locally or on a cloud provider)
- Git

### 2. Clone & Setup Backend

```bash
# Clone the repo
git clone https://github.com/yourusername/developershub.git
cd developershub/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your values
SECRET_KEY=your-very-secret-key-here
DATABASE_URL=postgresql://username:password@localhost/developershub
```

### 4. Create Database

```bash
# In psql
createdb developershub

# OR in psql shell
psql -U postgres
CREATE DATABASE developershub;
```

### 5. Seed the Database

```bash
python seed.py
```

This creates:
- Admin account: `admin@developershub.com` / `admin123`
- Sample services, portfolio items, and blog posts

### 6. Run the Backend

```bash
python app.py
# API running at http://localhost:5000
```

### 7. Run the Frontend

Open `frontend/index.html` in a browser, or serve it with:

```bash
# Using Python's built-in server
cd frontend
python -m http.server 3000
# Open http://localhost:3000
```

---

## API Endpoints

### Public Endpoints (no auth required)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/services/` | List all services |
| GET | `/api/portfolio/` | List all projects |
| GET | `/api/blog/` | List all blog posts |
| GET | `/api/blog/<id>` | Get single post |
| POST | `/api/contact/` | Submit inquiry |
| POST | `/api/bookings/` | Create booking |
| GET | `/api/bookings/available?date=` | Get available slots |

### Protected Endpoints (JWT required)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login` | Admin login |
| GET | `/api/auth/me` | Get current user |
| POST/PUT/DELETE | `/api/services/<id>` | Manage services |
| POST/PUT/DELETE | `/api/portfolio/<id>` | Manage portfolio |
| POST/PUT/DELETE | `/api/blog/<id>` | Manage blog posts |
| GET | `/api/contact/` | View all inquiries |
| PUT | `/api/contact/<id>/status` | Update inquiry status |
| GET | `/api/bookings/` | View all bookings |
| PUT | `/api/bookings/<id>/status` | Update booking status |

---

### Backend — Render / Railway (Production)
1. Push `backend/` to GitHub.
2. Link repo to Render/Railway.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
5. **CRITICAL Environment Variables**: 
   - `SECRET_KEY`: Set to a strong random hash.
   - `DATABASE_URL`: Your Supabase/Postgres connection string.
   - `ALLOWED_ORIGINS`: Set to your frontend domain (e.g. `https://developershub.com`).

### Frontend — Vercel / Netlify
1. The `API_BASE` in `main.js` is now dynamic and will automatically connect to `/api` on your production host.
2. Push `frontend/` to GitHub and link to Vercel/Netlify.
3. If the frontend is on a different domain than the backend, ensure the backend's `ALLOWED_ORIGINS` includes the frontend URL.


---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Backend | Python, Flask, Flask-CORS |
| Database | PostgreSQL with psycopg2 |
| Auth | JWT (PyJWT) + bcrypt |
| Deployment | Render (backend) + Vercel (frontend) |

---

## Features

**User-Facing**
- Dynamic services loaded from database
- Portfolio showcase with tech stack tags
- Blog with full article view
- Contact form with validation
- Meeting booking with time slot availability check

**Admin Panel**
- Secure JWT-based login
- Dashboard with live stats
- Full CRUD for Services, Portfolio, Blog
- View and manage client inquiries (mark read/resolved)
- View and manage bookings (confirm/cancel)

---

## Security
- Passwords hashed with bcrypt
- JWT tokens expire after 24 hours
- All admin routes protected with `@admin_required` decorator
- Form validation on both frontend and backend
- CORS configured for API access

---

*Built for DevelopersHub Corporation Full-Stack Internship Task*

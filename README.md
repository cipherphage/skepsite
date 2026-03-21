# Skepticamp NYC — Registration Site

Registration website for **Skepticamp NYC**, a free annual unconference organized by New York City Skeptics.

## Stack

- **Backend:** Django 4.2+ (Python)
- **Frontend:** Vue.js 3 (Composition API, progressive enhancement)
- **Database:** PostgreSQL
- **Build:** Vite 5

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+

### Setup

```bash
# 1. Clone and enter the repo
git clone <repo-url>
cd skepsite

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env with your local database credentials and a secret key

# 5. Run database migrations
python manage.py migrate

# 6. Create a superuser (for admin access)
python manage.py createsuperuser

# 7. Install frontend dependencies and build
npm install
npm run build

# 8. Run the development server
python manage.py runserver
```

The site will be at http://localhost:8000.

### Frontend Development

To watch for frontend changes during development:

```bash
npm run dev
```

Vite serves assets from `http://localhost:5173`. Update `base.html` to load from Vite dev server when developing Vue components.

## Commands

```bash
# Backend
python manage.py runserver           # Start dev server
python manage.py migrate             # Apply migrations
python manage.py makemigrations      # Create new migrations
python manage.py test                # Run all tests
python manage.py createsuperuser     # Create admin user
python manage.py check --deploy      # Pre-deployment checklist

# Frontend
npm run dev      # Start Vite dev server
npm run build    # Build for production → static/dist/
npm run lint     # Lint Vue components
```

## Architecture

```
skepsite/
  config/          Django project config (settings/, urls.py)
  apps/
    accounts/      Custom User model, MFA (TOTP), IP allowlisting
    registration/  Attendee / presenter / volunteer flows
    events/        Event model and data
    pages/         Home, About, Contact, Privacy
    communications/ Email utilities and logs
  templates/       Server-rendered HTML (Django templates)
  static/css/      Design tokens, components, animations, pages
  frontend/        Vue 3 components + Vite
    components/    ThemeToggle, CookieConsent, RegistrationWizard, etc.
    composables/   useTheme, useToast
```

## Settings

Settings are split by environment:

- `config/settings/base.py` — shared settings
- `config/settings/dev.py` — local development (`DEBUG=True`)
- `config/settings/production.py` — production hardening

Set `DJANGO_SETTINGS_MODULE` to choose the environment (default: `config.settings.dev`).

All secrets come from environment variables (via `python-decouple`). See `.env.example`.

## Admin Security

Admin access requires:

1. IP address in `ADMIN_ALLOWED_IPS` (set in `.env`)
2. Valid username + password
3. TOTP two-factor code (if a device is registered for the user)

Configure MFA via Django admin → OTP TOTP devices.

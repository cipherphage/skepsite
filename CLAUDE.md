# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Registration website for **Skepticamp NYC** — covering attendees, presenters, and volunteers. Run by New York City Skeptics (https://www.nycskeptics.org/).

## Stack

| Layer | Technology |
|---|---|
| Backend | Django (Python) |
| Frontend | Vue.js 3 (Composition API + `<script setup>`) |
| Database | PostgreSQL |
| Pattern | MVC — Vue enhances server-rendered pages, not a full SPA |

Vue.js is used **progressively**: Django renders HTML templates; Vue mounts on specific elements for interactivity (forms, theme toggle, dynamic components). Do not turn this into a single-page application with a separate API layer unless a feature genuinely requires it.

## Commands

> Commands will be added here as the project is scaffolded. Expected structure:

```bash
# Backend
python manage.py runserver
python manage.py migrate
python manage.py test                          # all tests
python manage.py test <app>.tests.<TestClass>  # single test class

# Frontend
npm run dev      # or equivalent once build tooling is chosen
npm run build
npm run lint

# Database
python manage.py makemigrations
python manage.py createsuperuser
```

## Intended Architecture

```
skepsite/
  config/                  ← Django project config (settings/, urls.py, wsgi.py)
    settings/
      base.py              ← shared settings
      dev.py               ← DEBUG=True, SQLite or local Postgres
      production.py        ← SECURE_*, production DB, email backend
  apps/
    accounts/              ← custom user model, MFA, IP whitelisting, admin auth
    registration/          ← attendee / presenter / volunteer registration flows
    events/                ← event info (date, location, schedule)
    pages/                 ← static-ish pages: About, Contact
    communications/        ← Gmail integration, transactional email
  templates/               ← project-level base templates + includes
  static/                  ← project-level static assets (CSS, compiled JS)
  frontend/                ← Vue components and build tooling (Vite)
```

Django apps own their models, views, URLs, forms, and templates. Vue components live in `frontend/` and are built into `static/`. Each template mounts Vue only where needed via `<div id="...">` entry points.

## Key Design Decisions

**Custom User Model** — must be defined before the first migration. Extend `AbstractBaseUser` or `AbstractUser` in `apps/accounts/`. Do not use the default `auth.User` directly.

**Settings split** — all environment-specific config goes in `config/settings/dev.py` or `config/settings/production.py`, both inheriting from `base.py`. `SECRET_KEY`, database credentials, and email credentials come from environment variables — never hardcoded.

**MFA and IP whitelisting** — admin users require TOTP-based MFA and must be on an allowlisted IP range. Implement as Django middleware or a custom `AdminSite` subclass.

**Gmail integration** — use Django's email backend system. Store OAuth credentials (or app password) in environment variables. Admin configures their account through a settings UI, not by editing code.

**Theme toggle** — light/dark preference stored in `localStorage` and applied via a CSS class on `<html>`. Django renders a `prefers-color-scheme` fallback; Vue manages the toggle interaction.

**Cookie consent** — non-essential cookies (analytics, preferences beyond theme) require explicit opt-in. Fully GDPR/CCPA compliant: opt-out must be as easy as opt-in.

**ADA compliance** — semantic HTML throughout (`<nav>`, `<main>`, `<section>`, `<article>`, `<button>` not `<div>`), WCAG 2.1 AA contrast ratios, full keyboard navigation, ARIA labels on interactive elements. Every Vue component must remain keyboard and screen-reader accessible.

## Skills

Use any skills you need, but these are specifically recommended for this stack:

- `/django` — models, QuerySets, views, forms, settings, testing
- `/vuejs` — Composition API, composables, reactivity, progressive enhancement
- `/python-design-patterns` — Python idioms for service layer and utilities
- `/python-data-structures` — correct Python collection usage
- `/refactoring` — keeping code clean as the project grows

## Reference

- Existing site (features/content reference only): https://skepticampnyc.org/
- NYC Skeptics org: https://www.nycskeptics.org/
- UI inspiration (design approach, not copy): https://apple.com, https://eventbrite.com
- Django docs: https://docs.djangoproject.com/
- Vue.js docs: https://vuejs.org/

# K&K Trading Company — Corporate Website

A modern, premium corporate portfolio website built with **Django** (server-rendered templates), designed to be fully managed by non-developers through **Django Admin**.

This is a company showcase site — not an e-commerce platform. There is no cart, checkout, or payment processing anywhere in the project.

---

## Tech Stack

- **Backend:** Python, Django, Django ORM, Django Forms, Django Admin
- **Frontend:** Django Templates, HTML5, CSS3 (hand-written design system, no framework), vanilla JavaScript
- **Database:** SQLite (local development) / PostgreSQL (production, via `DATABASE_URL`)
- **Static files:** WhiteNoise (production-ready static serving with compression)

---

## Project Structure

```text
kandk/
├── manage.py
├── requirements.txt
├── .env.example
├── config/                 # Django project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── core/                    # Main application
│   ├── models.py            # CompanyProfile, Service, Product, Project, etc.
│   ├── views.py
│   ├── urls.py
│   ├── forms.py             # Enquiry form (with honeypot spam protection)
│   ├── admin.py              # Django Admin configuration
│   ├── middleware.py         # Enquiry rate limiting
│   ├── context_processors.py # Makes CompanyProfile available in every template
│   ├── sitemaps.py
│   └── management/commands/seed_demo_data.py
├── templates/
│   ├── base.html
│   ├── 404.html / 500.html
│   └── core/                # home, about, services, products, projects, contact
├── static/
│   ├── css/main.css          # Design system
│   └── js/main.js            # Nav, reveal animations, counters, FAQ accordion
└── media/                    # User-uploaded images (via Django Admin)
```

---

## 1. Installation

### Linux / macOS / WSL

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 2. Environment Variables

Copy the example file and fill in real values before deploying:

```bash
cp .env.example .env
```

```env
SECRET_KEY=
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DATABASE_URL=

EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=
COMPANY_EMAIL=
```

- Leave `DATABASE_URL` empty to use local SQLite. For PostgreSQL in production, set it to something like:
  `postgres://USER:PASSWORD@HOST:PORT/NAME`
- `COMPANY_EMAIL` is the address that receives enquiry notifications — change it any time without touching code.
- If `EMAIL_HOST_USER` is left empty while `DEBUG=True`, emails are printed to the console instead of sent, so you can test the enquiry flow without real SMTP credentials.
- Works with Gmail SMTP, Microsoft 365, SendGrid, Amazon SES, or Brevo — just set the standard `EMAIL_HOST` / `EMAIL_PORT` / credentials for whichever provider you use.

---

## 3. Database

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 4. Create an Admin Account

```bash
python manage.py createsuperuser
```

---

## 5. (Optional) Seed Placeholder Demo Content

So the site looks complete immediately after setup:

```bash
python manage.py seed_demo_data
```

**Important:** every value this command creates is explicitly marked `[Placeholder]` and uses made-up figures (years of experience, client counts, project history, etc.). None of it is real company data — replace all of it from Django Admin before launching publicly.

---

## 6. Run the Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` for the site and `http://127.0.0.1:8000/admin/` for the content manager.

---

## Content Management

Everything editors are expected to change lives in Django Admin — nothing is hard-coded in templates:

| Admin Section | Controls |
|---|---|
| Company Profile | Name, tagline, logo, hero text, contact info, social links, mission/vision |
| Services | Business areas shown on Home and the Services page |
| Product Categories / Products | Product catalogue (view + enquire only — no cart or checkout) |
| Project Categories / Projects | Portfolio / business activities, with image galleries |
| Team Members | Leadership section on the About page |
| Testimonials | Client quotes shown on the homepage |
| Statistics | The animated counters (years of experience, clients, etc.) |
| Timeline Events | The "Our Story" timeline on the About page |
| Core Values | The "Why Choose Us" / values section |
| FAQ | Accordion on the Contact page |
| Enquiries | Read-only log of every form submission, with a status workflow (New → Contacted → In Progress → Resolved) |

Only items marked **Active/Published** appear on the public site, and only items marked **Featured** appear on the homepage.

---

## Enquiry Form

- Validates required fields (name, email, subject, message) with Django Forms
- Saves every submission to the database (visible and searchable in Django Admin)
- Emails the configured `COMPANY_EMAIL` address — if the email fails to send, the enquiry is still saved safely, so nothing is lost
- Includes a hidden honeypot field to filter out basic bots
- A lightweight middleware rate-limits submissions per IP (max 5 per 10 minutes, 30-second cooldown between attempts) — no external service required
- The submit button disables itself on click client-side to avoid accidental duplicate submissions

---

## Production Checklist

Before deploying:

1. Set `DEBUG=False` and a strong, unique `SECRET_KEY`.
2. Set `ALLOWED_HOSTS` to your real domain(s).
3. Point `DATABASE_URL` at your PostgreSQL instance.
4. Set real SMTP credentials and `COMPANY_EMAIL`.
5. Run `python manage.py collectstatic` (WhiteNoise serves compressed static files).
6. Serve with a production WSGI server, e.g. `gunicorn config.wsgi:application`.
7. Put the site behind HTTPS — `SECURE_SSL_REDIRECT`, secure cookies, and HSTS are already enabled automatically whenever `DEBUG=False`.
8. Replace every placeholder image/text seeded by `seed_demo_data` with real company content.

---

## Notes on Design

- Color palette, typography, and spacing live entirely in `static/css/main.css` as CSS custom properties (`:root`), so the whole visual identity can be re-themed without touching HTML.
- Animations respect `prefers-reduced-motion` and are capped around 300–700ms as specified.
- The site uses Google Fonts (Fraunces for display headings, Inter for body text) and Bootstrap Icons via CDN — both require the visitor's browser to have normal internet access, same as any production website.

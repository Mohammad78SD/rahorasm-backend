# RahoRasm Backend

Django REST API for **RahoRasm**, a Persian-language tour booking platform: tours with flights and hotel pricing, visa information, a blog, OTP-based phone authentication with JWT, and a reservation flow.

The web frontend is a separate Nuxt project: [Mohammad78SD/rahorasm](https://github.com/Mohammad78SD/rahorasm).

> TODO: add a live demo URL and screenshots (e.g. Django admin and API responses).

## Features

- **Tours**: catalogue organised by continent, country and city; flight legs and flight times; hotel price options; featured tours, occasion tags, filtering by destination and price; navbar and home-page aggregate endpoints; per-tour PDF export (WeasyPrint).
- **Hotels**: hotels with images, star rating and several facility groups (hotel, room, recreational, sport); per-room-type pricing (double, single, child with/without bed, infant) with an optional second currency (EUR/USD).
- **Reservations**: authenticated users create reservations for a flight time and hotel price, with passenger details (names, national code, passport, birth date) and a computed final price. Status values: `review`, `pending`, `paid`, `canceled`.
- **Authentication**: phone number as the username; password login, or OTP login and signup delivered by SMS (IPPanel); JWT access/refresh tokens.
- **Visa**: visa pages per country with Q&A entries.
- **Blog**: categories, posts and comments (CKEditor 5 rich text).
- **Site content**: contact details, about-us entries, footer columns and contact form submissions, editable from the admin.
- **Admin**: Django admin with Persian labels, Jalali (Persian calendar) date fields and nested inlines.

## Tech stack

- Python, Django 5.1, Django REST Framework
- `djangorestframework-simplejwt` (JWT), `django-filter`, `django-cors-headers`
- PostgreSQL (`psycopg2`), Redis cache (`django-redis`)
- `django-ckeditor-5`, `django-jalali`, `django-nested-admin`
- WeasyPrint (PDF), `ippanel` (SMS), Pillow

## Project layout

The Django project lives in `rahorasm/` (settings in `rahorasm/rahorasm/settings.py`).

| App | Responsibility | Key models |
| --- | --- | --- |
| `UserManager` | Custom user model, OTP/password auth, profile, contact form | `UserModel`, `ContactForm` |
| `TourManager` | Tours, geography, flights, listing/filter/home endpoints, PDF | `Tour`, `FlightTimes`, `FlightLeg`, `Airport`, `AirLine`, `City`, `Country`, `Continent` |
| `HotelManager` | Hotels and room pricing | `Hotel`, `HotelPrice`, `HotelImage`, facility models |
| `ReserveManager` | Reservations and passengers | `Reserve`, `Person` |
| `VisaManager` | Visa information | `Visa`, `Question` |
| `blog` | Blog | `Category`, `Post`, `Comment` |
| `misc` | Site-wide content | `ContactDetail`, `AboutDetail`, `FooterBody`, `FooterColumn`, `FooterContact`, `MainPagePDF` |

## API endpoints

Routes are derived from the URL configuration. Auth column: JWT = `Authorization: Bearer <access token>` required.

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| POST | `/token/` | - | Obtain JWT pair (SimpleJWT) |
| POST | `/token/refresh/` | - | Refresh access token |
| POST | `/auth/login` | - | Phone + password login |
| POST | `/auth/login/request` | - | Send login OTP by SMS |
| POST | `/auth/login/validate` | - | Verify login OTP, returns tokens |
| POST | `/auth/signup/request` | - | Start signup, send OTP |
| POST | `/auth/signup/validate` | - | Verify OTP, create user, returns tokens |
| GET | `/auth/user-session` | JWT | Current user summary |
| GET, PUT | `/auth/user-profile` | JWT | Read / update profile |
| POST | `/auth/contact-us` | - | Submit contact form |
| GET | `/tour/tours/` | - | List tours (filter by city, country, continent, featured, occasion, ...) |
| GET | `/tour/tour/<id>/` | - | Tour detail |
| GET | `/tour/flights/<id>/` | - | Flights for a tour |
| GET | `/tour/flight/<id>/` | - | Flight detail |
| GET | `/tour/pdf/<id>/` | - | Tour as PDF |
| GET | `/tour/cities/`, `/tour/countries/`, `/tour/airlines/`, `/tour/airports/` | - | Reference lists (name filters) |
| GET | `/tour/filters/` | - | Available filter values |
| GET | `/tour/navbar/`, `/tour/home/` | - | Aggregated data for navbar / home page |
| GET | `/hotels/`, `/hotels/<id>/` | - | Hotel list / detail |
| POST | `/reserve/new/` | JWT | Create a reservation |
| GET | `/reserve/list/`, `/reserve/<id>/` | JWT | The user's reservations |
| GET | `/visa/list/`, `/visa/search/`, `/visa/<id>/` | - | Visa list, search, detail |
| GET | `/blog/posts/`, `/blog/posts/<id>/` | - | Posts |
| GET, POST | `/blog/posts/<post_id>/comments/` | - | Comments |
| GET | `/api/contactus/`, `/api/aboutus/`, `/api/footer/` | - | Site content |
| - | `/admin/`, `/ckeditor5/` | - | Admin site, editor uploads |

## Authentication

Authentication is JWT-only (`rest_framework_simplejwt` is the sole DRF authentication class). Access tokens last 5 minutes and refresh tokens 1 day, with refresh rotation and blacklisting enabled in settings. OTP codes (6 digits, 5-minute expiry, 60-second resend cooldown) and pending signup data are stored in the Redis cache and sent by SMS through IPPanel.

## Getting started

Prerequisites: Python 3.12 (the version the project was developed on), PostgreSQL, Redis, and the system libraries WeasyPrint needs (Pango).

```bash
git clone https://github.com/Mohammad78SD/rahorasm-backend.git
cd rahorasm-backend

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cd rahorasm
cp ../.env.example .env      # then edit the values
python manage.py migrate
python manage.py createsuperuser   # prompts for phone number and password
python manage.py runserver
```

The API is then available at http://127.0.0.1:8000/ and the admin at http://127.0.0.1:8000/admin/.

For local HTTP development set `DEBUG=True` and `CSRF_COOKIE_SECURE=False` / `SESSION_COOKIE_SECURE=False` in `.env`.

Note: the pinned `psycopg2==2.9.9` does not build from source on Python 3.13+; use Python 3.12 or install `psycopg2-binary`.

## Environment variables

Settings are read with `django-environ` from `rahorasm/.env` (see `.env.example`) or the process environment.

| Variable | Required | Default | Purpose |
| --- | --- | --- | --- |
| `SECRET_KEY` | yes | - | Django secret key |
| `JWT` | yes | - | JWT signing key |
| `DEBUG` | no | `False` | Django debug mode |
| `ALLOWED_HOSTS` | no | empty | Comma-separated hosts |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD` | yes | - | PostgreSQL credentials |
| `DB_HOST`, `DB_PORT` | no | `localhost`, `5432` | PostgreSQL location |
| `REDIS_URL` | no | `redis://127.0.0.1:6379/2` | Cache (OTP storage) |
| `CORS_ALLOWED_ORIGINS` | no | empty | Comma-separated frontend origins |
| `CORS_ALLOW_ALL_ORIGINS` | no | `False` | Allow any origin (dev only) |
| `CSRF_TRUSTED_ORIGINS` | no | empty | Comma-separated trusted origins |
| `CSRF_COOKIE_SECURE`, `SESSION_COOKIE_SECURE` | no | `True` | Require HTTPS for cookies |
| `IPPANEL_API_KEY` | for SMS | empty | IPPanel API key |
| `IPPANEL_ORIGINATOR` | no | `+983000505` | SMS sender line |
| `IPPANEL_OTP_PATTERN` | for OTP | empty | IPPanel pattern code for OTP |
| `IPPANEL_NOTIFY_PATTERN` | no | empty | Pattern code for `send_sms` helper |
| `STATIC_ROOT`, `MEDIA_ROOT` | no | `<project>/staticfiles`, `<project>/media` | File locations |

## Status and limitations

- No online payment gateway is integrated; the `paid` reservation status exists but is set manually (admin).
- Test modules are present but contain no tests yet.

## License

TODO: add a license.

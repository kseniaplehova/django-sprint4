# Blogicum — Sprint 4: full blog

A multi-user blog built with Django: registration, posts with images, comments, user profiles, pagination and custom error pages.

Educational project — Yandex Practicum, Python Developer course. This is the **final stage (3 of 3)** of the Blogicum project (earlier stages: `django-sprint1`, `django-sprint3`).

## Features

- Models `Post` (with optional image upload), `Category`, `Location` and `Comment`, sharing abstract base models.
- Class-based views for the post list, post detail, category page, profile, and post create / edit / delete; function views with `@login_required` for comment create / edit / delete.
- Authors can edit and delete only their own posts and comments; others are redirected or get 404. Authors also see their own unpublished or scheduled posts.
- User registration, login / logout, password change and reset (Django auth, templates in `registration/`), profile editing.
- Pagination (10 posts per page); comment counts annotated in the queryset.
- Custom 403 (CSRF), 404 and 500 pages; forms rendered with `django-bootstrap5`; e-mails written to files in development.
- Admin with inline comments on posts.

## Tech stack

Python, Django 5.1.1, django-bootstrap5, Pillow, SQLite, pytest, pytest-django, mixer, flake8 (see `requirements.txt`).

## Getting started

```bash
git clone https://github.com/kseniaplehova/django-sprint4.git
cd django-sprint4
python -m venv venv
source venv/Scripts/activate   # Windows (Git Bash); on Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
cd blogicum
python manage.py migrate
python manage.py loaddata ../db.json   # optional demo data
python manage.py runserver
```

## Tests

From the repository root:

```bash
pytest
```

The suite in `tests/` checks posts, comments, editing permissions, users, e-mails, static and error pages, and page content.

## Author

Ksenia Plehova — [GitHub](https://github.com/kseniaplehova)

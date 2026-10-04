"""Settings for the test suite: sqlite + in-memory cache, dummy secrets.

Used via pytest.ini (DJANGO_SETTINGS_MODULE=rahorasm.test_settings). No real
database, Redis or SMS provider is needed. All values below are dummies.
"""
import os

os.environ.setdefault("SECRET_KEY", "test-only-secret-key")
os.environ.setdefault("JWT", "test-only-jwt-signing-key")
os.environ.setdefault("DB_NAME", "unused")
os.environ.setdefault("DB_USER", "unused")
os.environ.setdefault("DB_PASSWORD", "unused")

from .settings import *  # noqa: E402,F401,F403

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
IPPANEL_API_KEY = "dummy"
IPPANEL_OTP_PATTERN = "dummy"

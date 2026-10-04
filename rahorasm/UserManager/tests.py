from unittest import mock

from django.conf import settings
from django.core.cache import cache
from django.urls import reverse
from rest_framework.test import APITestCase

from test_helpers import make_user
from .models import UserModel

PHONE = "09121112233"


class AuthTestBase(APITestCase):
    def setUp(self):
        cache.clear()  # throttle counters and OTP state live in the cache
        patcher = mock.patch("UserManager.views.send_otp")  # never hit IPPanel
        self.send_otp = patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(cache.clear)

    def issued_otp(self):
        return cache.get(f"otp_{PHONE}")


class PasswordLoginTests(AuthTestBase):
    def test_login_success(self):
        make_user(PHONE, "secret-pass-1")
        resp = self.client.post(reverse("login"), {"phone_number": PHONE, "password": "secret-pass-1"})
        self.assertEqual(resp.status_code, 200)
        self.assertIn("access", resp.json())

    def test_login_wrong_password(self):
        make_user(PHONE, "secret-pass-1")
        resp = self.client.post(reverse("login"), {"phone_number": PHONE, "password": "nope"})
        self.assertEqual(resp.status_code, 400)

    def test_login_is_throttled(self):
        make_user(PHONE, "secret-pass-1")
        for _ in range(10):
            self.assertEqual(self.client.post(reverse("login"), {"phone_number": PHONE, "password": "x"}).status_code, 400)
        self.assertEqual(self.client.post(reverse("login"), {"phone_number": PHONE, "password": "x"}).status_code, 429)

    def test_token_endpoint_is_throttled(self):
        make_user(PHONE, "secret-pass-1")
        codes = [self.client.post(reverse("token_obtain_pair"), {"phone_number": PHONE, "password": "x"}).status_code
                 for _ in range(11)]
        self.assertEqual(codes[:10], [401] * 10)
        self.assertEqual(codes[10], 429)


class OtpLoginTests(AuthTestBase):
    def test_request_unknown_user_404(self):
        resp = self.client.post(reverse("login_request_otp"), {"phone_number": PHONE})
        self.assertEqual(resp.status_code, 404)
        self.send_otp.assert_not_called()

    def test_request_sends_sms_once_and_cooldown_blocks_repeat(self):
        make_user(PHONE)
        url = reverse("login_request_otp")
        self.assertEqual(self.client.post(url, {"phone_number": PHONE}).status_code, 200)
        self.send_otp.assert_called_once_with(PHONE, self.issued_otp())
        self.assertEqual(self.client.post(url, {"phone_number": PHONE}).status_code, 429)
        self.assertEqual(self.send_otp.call_count, 1)

    def test_validate_correct_otp_returns_tokens_and_consumes_otp(self):
        make_user(PHONE)
        self.client.post(reverse("login_request_otp"), {"phone_number": PHONE})
        otp = self.issued_otp()
        resp = self.client.post(reverse("login_validate_otp"), {"phone_number": PHONE, "otp": otp})
        self.assertEqual(resp.status_code, 200)
        self.assertIn("refresh", resp.json())
        self.assertIsNone(self.issued_otp())

    def test_validate_wrong_otp_400(self):
        make_user(PHONE)
        self.client.post(reverse("login_request_otp"), {"phone_number": PHONE})
        resp = self.client.post(reverse("login_validate_otp"), {"phone_number": PHONE, "otp": "000000"})
        self.assertIn(resp.status_code, (400,))

    def test_otp_locked_after_max_tries_even_with_correct_code(self):
        make_user(PHONE)
        self.client.post(reverse("login_request_otp"), {"phone_number": PHONE})
        otp = self.issued_otp()
        wrong = "000000" if otp != "000000" else "111111"
        url = reverse("login_validate_otp")
        for _ in range(settings.MAX_OTP_TRY):
            self.assertEqual(self.client.post(url, {"phone_number": PHONE, "otp": wrong}).status_code, 400)
        resp = self.client.post(url, {"phone_number": PHONE, "otp": otp})
        self.assertEqual(resp.status_code, 429)
        self.assertNotIn("access", resp.json())

    def test_new_otp_resets_attempt_counter(self):
        make_user(PHONE)
        req, val = reverse("login_request_otp"), reverse("login_validate_otp")
        self.client.post(req, {"phone_number": PHONE})
        for _ in range(settings.MAX_OTP_TRY):
            self.client.post(val, {"phone_number": PHONE, "otp": "000000"})
        cache.delete(f"otp_cooldown_{PHONE}")  # skip the 60s resend wait
        self.client.post(req, {"phone_number": PHONE})
        resp = self.client.post(val, {"phone_number": PHONE, "otp": self.issued_otp()})
        self.assertEqual(resp.status_code, 200)

    def test_otp_request_is_throttled(self):
        make_user(PHONE)
        url = reverse("login_request_otp")
        for _ in range(5):
            cache.delete(f"otp_cooldown_{PHONE}")
            self.assertEqual(self.client.post(url, {"phone_number": PHONE}).status_code, 200)
        cache.delete(f"otp_cooldown_{PHONE}")
        self.assertEqual(self.client.post(url, {"phone_number": PHONE}).status_code, 429)
        self.assertEqual(self.send_otp.call_count, 5)

    def test_otp_validate_is_throttled(self):
        url = reverse("login_validate_otp")
        codes = [self.client.post(url, {"phone_number": f"0912000{i:04d}", "otp": "123456"}).status_code
                 for i in range(11)]
        self.assertEqual(codes[:10], [400] * 10)
        self.assertEqual(codes[10], 429)


class SignupTests(AuthTestBase):
    data = {"phone_number": PHONE, "password": "a-good-pass-1", "name": "Test User"}

    def test_signup_flow_creates_user(self):
        self.assertEqual(self.client.post(reverse("signup_request"), self.data).status_code, 200)
        self.send_otp.assert_called_once()
        resp = self.client.post(reverse("signup_validate_otp"), {"phone_number": PHONE, "otp": self.issued_otp()})
        self.assertEqual(resp.status_code, 201)
        user = UserModel.objects.get(phone_number=PHONE)
        self.assertEqual(user.name, "Test User")
        self.assertTrue(user.check_password("a-good-pass-1"))

    def test_signup_existing_phone_rejected(self):
        make_user(PHONE)
        self.assertEqual(self.client.post(reverse("signup_request"), self.data).status_code, 400)
        self.send_otp.assert_not_called()

    def test_signup_wrong_otp_locks_after_max_tries(self):
        self.client.post(reverse("signup_request"), self.data)
        otp = self.issued_otp()
        wrong = "000000" if otp != "000000" else "111111"
        url = reverse("signup_validate_otp")
        for _ in range(settings.MAX_OTP_TRY):
            self.assertEqual(self.client.post(url, {"phone_number": PHONE, "otp": wrong}).status_code, 400)
        self.assertEqual(self.client.post(url, {"phone_number": PHONE, "otp": otp}).status_code, 429)
        self.assertFalse(UserModel.objects.filter(phone_number=PHONE).exists())

    def test_signup_request_cooldown_blocks_repeat(self):
        url = reverse("signup_request")
        self.assertEqual(self.client.post(url, self.data).status_code, 200)
        self.assertEqual(self.client.post(url, self.data).status_code, 429)
        self.assertEqual(self.send_otp.call_count, 1)
        cache.delete(f"otp_cooldown_{PHONE}")
        self.assertEqual(self.client.post(url, self.data).status_code, 200)
        self.assertEqual(self.send_otp.call_count, 2)


class ProfileTests(AuthTestBase):
    def setUp(self):
        super().setUp()
        self.user = make_user(PHONE, "old-pass-123", name="Old")
        self.client.force_authenticate(self.user)
        self.url = reverse("user_profile")

    def test_update_name_and_email_keeps_password(self):
        """Regression: the stored hash used to be re-hashed, locking the user out."""
        resp = self.client.put(self.url, {"name": "New", "email": "a@b.co"})
        self.assertEqual(resp.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual((self.user.name, self.user.email), ("New", "a@b.co"))
        self.assertTrue(self.user.check_password("old-pass-123"))
        self.client.force_authenticate(None)
        resp = self.client.post(reverse("login"), {"phone_number": PHONE, "password": "old-pass-123"})
        self.assertEqual(resp.status_code, 200)

    def test_password_change_requires_current_password(self):
        resp = self.client.put(self.url, {"password": "brand-new-1"})
        self.assertEqual(resp.status_code, 400)
        resp = self.client.put(self.url, {"password": "brand-new-1", "current_password": "wrong"})
        self.assertEqual(resp.status_code, 400)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("old-pass-123"))

    def test_password_change_with_current_password(self):
        resp = self.client.put(self.url, {"password": "brand-new-1", "current_password": "old-pass-123"})
        self.assertEqual(resp.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("brand-new-1"))


class SessionTests(AuthTestBase):
    def test_user_session_requires_auth(self):
        self.assertEqual(self.client.get(reverse("user_session")).status_code, 401)

    def test_user_session_ok(self):
        self.client.force_authenticate(make_user(PHONE))
        self.assertEqual(self.client.get(reverse("user_session")).status_code, 200)

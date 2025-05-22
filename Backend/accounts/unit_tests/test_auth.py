"""Testing for account/views.py: Got sidetracked with csrf_tokens and sessionid cookies, but testing covers
basic functionality"""

from rest_framework.test import APITestCase, APIClient
from rest_framework.response import Response
from django.urls import reverse
from django.contrib.auth.models import User
from http.cookies import Morsel
from user_habit_tracker.models import HabitTrackerUser, Habit


class AuthTestCase(APITestCase):
    def setUp(self) -> None:
        self.csrf_client = APIClient(enforce_csrf_checks=True)

    def check_cannot_access_resource_when_not_logged_in(self) -> None:
        whoami_url: str = reverse("api-whoami")
        whoami_response_bad: Response = self.client.get(
            whoami_url,
            format="json",
        )
        self.assertEqual(whoami_response_bad.status_code, 403)

    def test_get_csrf(self) -> None:
        url: str = reverse("api-csrf")
        response: Response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("X-CSRFToken", response.headers)

        # Usually both are equal, due to me changing the settings of the CSRF_Cookie by specifying
        # CSRF_COOKIE_SAMESITE and CSRF_COOKIE_HTTPONLY in settings.py they are different as csrf_cookie
        # is now encoding more data, but the "csrf" values are the same decoded.
        csrf_token: str | None = response.headers.get("X-CSRFToken")
        csrf_cookie: Morsel[str] | None = response.cookies.get("csrftoken")

        assert csrf_token is not None, "CSRF token not found in response"
        assert csrf_cookie is not None, "CSRF cookie not found in response"

        # Check that the cookie value and the token is non-empty: empty strings are treated as false
        self.assertTrue(csrf_token)
        self.assertTrue(csrf_cookie.value)

        # Check SameSite settings
        self.assertEqual(csrf_cookie["samesite"].lower(), "strict")
        self.assertEqual(csrf_cookie["httponly"], "")

    def test_login_view(self) -> None:

        self.check_cannot_access_resource_when_not_logged_in()
        url: str = reverse("api-login")

        User.objects.create_user(username="<USERNAME>", password="<PASSWORD>")
        HabitTrackerUser.objects.create(author=User.objects.get(username="<USERNAME>"))

        # Check that login works correctly
        wrong_credentials_response: Response = self.csrf_client.post(
            url,
            data={
                "username": "<username>",
                "password": "<password>",
            },
            format="json",
        )
        self.assertEqual(wrong_credentials_response.status_code, 401)

        missing_password_response: Response = self.csrf_client.post(
            url,
            data={
                "username": "<username>",
            },
            format="json",
        )
        self.assertEqual(missing_password_response.status_code, 400)

        missing_username_response: Response = self.csrf_client.post(
            url,
            data={
                "password": "<password>",
            },
            format="json",
        )
        self.assertEqual(missing_username_response.status_code, 400)

        response: Response = self.csrf_client.post(
            url,
            data={
                "username": "<USERNAME>",
                "password": "<PASSWORD>",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)

        # Check validity of CSRF cookie (using post method since csrf token is required)
        csrf_url: str = reverse("api-csrf")
        csrf_response: Response = self.csrf_client.get(csrf_url)
        csrf_token: str | None = csrf_response.headers.get("X-CSRFToken")
        assert csrf_token is not None, "CSRF token not found in response"

        csrf_invalid_response: Response = self.csrf_client.post(
            path="/api/habits/",
            data={
                "title": "Habit",
                "text": "Do Something Daily",
            },
            format="json",
            HTTP_X_CSRFTOKEN=csrf_token + "invalid",
        )
        self.assertEqual(csrf_invalid_response.status_code, 403)
        self.assertEqual(Habit.objects.count(), 0)

        csrf_valid_response: Response = self.csrf_client.post(
            path="/api/habits/",
            data={
                "title": "Habit",
                "text": "Do Something Daily",
            },
            format="json",
            HTTP_X_CSRFTOKEN=csrf_token,
        )

        self.assertEqual(csrf_valid_response.status_code, 201)
        self.assertEqual(Habit.objects.count(), 1)

        # Check validity of session cookie (using get method since session cookie is required)
        session_cookie: Morsel[str] | None = response.cookies.get("sessionid")
        assert session_cookie is not None, "Session cookie not found in response"
        self.assertTrue(session_cookie.value)
        self.assertEqual(session_cookie["samesite"].lower(), "strict")
        self.assertEqual(session_cookie["httponly"], True)

        whoami_url: str = reverse("api-whoami")

        session_invalid_response: Response = self.client.get(
            path=whoami_url,
            format="json",
        )
        self.assertEqual(session_invalid_response.status_code, 403)

        session_valid_response: Response = self.client.get(
            path=whoami_url,
            format="json",
            HTTP_COOKIE=f"sessionid={session_cookie.value}",
        )
        self.assertEqual(session_valid_response.status_code, 200)

    def test_logout_view(self) -> None:
        self.check_cannot_access_resource_when_not_logged_in()
        whoami_url: str = reverse("api-whoami")

        # Test logging out when you haven't logged in yet
        logout_url: str = reverse("api-logout")
        logout_response_bad: Response = self.client.post(
            logout_url,
            format="json",
        )

        self.assertEqual(logout_response_bad.status_code, 403)

        # Test logging out when you have logged in
        login_url: str = reverse("api-login")
        User.objects.create_user(username="<USERNAME>", password="<PASSWORD>")
        HabitTrackerUser.objects.create(author=User.objects.get(username="<USERNAME>"))

        login_response: Response = self.client.post(
            login_url,
            data={
                "username": "<USERNAME>",
                "password": "<PASSWORD>",
            },
            format="json",
        )
        self.assertEqual(login_response.status_code, 200)
        self.assertIn("sessionid", login_response.cookies)
        session_id: Morsel[str] | None = login_response.cookies.get("sessionid")
        assert session_id is not None, "Session cookie not found in response"
        self.assertNotEqual(session_id.value, "")

        # Check you can access resource when you are logged in
        whoami_response_when_logged_in: Response = self.client.get(
            whoami_url,
            format="json",
        )

        self.assertEqual(whoami_response_when_logged_in.status_code, 200)

        logout_response_good: Response = self.client.post(
            logout_url,
            format="json",
        )
        self.assertEqual(logout_response_good.status_code, 200)
        self.assertEqual(
            logout_response_good.data.get("detail"), "Successfully logged out"
        )

        # Check that you can't access resource when you are logged out
        whoami_response_bad_second: Response = self.client.get(
            whoami_url,
            format="json",
        )
        self.assertEqual(whoami_response_bad_second.status_code, 403)
        session_id_two = whoami_response_bad_second.cookies.get("sessionid")
        assert session_id_two is not None, "Session cookie not found in response"
        self.assertEqual(session_id_two.value, "")

    def test_register_view(self) -> None:
        # In this case confirms you are not logged in
        self.check_cannot_access_resource_when_not_logged_in()

        # Check that register works correctly
        User.objects.create_user(username="<USERNAME>", password="<PASSWORD>")
        HabitTrackerUser.objects.create(author=User.objects.get(username="<USERNAME>"))

        register_url: str = reverse("api-register")

        register_response_existing_user: Response = self.client.post(
            register_url,
            data={
                "username": "<USERNAME>",
                "password": "<PASSWORD>",
            },
            format="json",
        )

        self.assertEqual(register_response_existing_user.status_code, 400)
        self.assertEqual(
            register_response_existing_user.data.get("error"), "User already exists"
        )

        register_response_missing_password: Response = self.client.post(
            register_url,
            data={
                "username": "<USERNAME>",
            },
            format="json",
        )

        self.assertEqual(register_response_missing_password.status_code, 400)
        self.assertEqual(
            register_response_missing_password.data.get("error"),
            "Please provide both username and password",
        )

        register_response_missing_username: Response = self.client.post(
            register_url,
            data={
                "password": "<PASSWORD>",
            },
            json="json",
        )

        self.assertEqual(register_response_missing_username.status_code, 400)
        self.assertEqual(
            register_response_missing_username.data.get("error"),
            "Please provide both username and password",
        )

        register_response_good: Response = self.client.post(
            register_url,
            data={
                "username": "<username>",
                "password": "<password>",
            },
            format="json",
        )

        self.assertEqual(register_response_good.status_code, 201)

        # Confirm that registering user also logs in you in
        whoami_url: str = reverse("api-whoami")
        whoami_response: Response = self.client.get(
            whoami_url,
            format="json",
        )

        self.assertEqual(whoami_response.status_code, 200)
        self.assertEqual(whoami_response.data.get("username"), "<username>")

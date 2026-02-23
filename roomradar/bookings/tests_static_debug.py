from django.test import TestCase, Client
from django.contrib.staticfiles.finders import find

class StaticFileAccessibilityTests(TestCase):
    def test_static_file_finder(self):
        # Verify Django can find the file internally
        found_path = find('bookings/css/teacherDashboard.css')
        self.assertIsNotNone(found_path, "Static file not found by finder")
        print(f"DEBUG: Found static file at {found_path}")

    def test_static_url_reachable(self):
        # Verify the file is served via HTTP
        c = Client()
        # This assumes STATIC_URL is /static/
        response = c.get('/static/bookings/css/teacherDashboard.css')
        if response.status_code == 404:
            print("DEBUG: HTTP 404 for static file")
        else:
            print(f"DEBUG: HTTP {response.status_code} for static file")

        # Note: Client might not serve static files unless using StaticLiveServerTestCase or similar,
        # but let's see what happens. Standard Client usually doesn't serve static.

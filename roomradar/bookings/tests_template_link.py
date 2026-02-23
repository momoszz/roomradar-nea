from django.test import TestCase, Client
from django.contrib.auth.models import User

class TemplateStaticLinkTests(TestCase):
    def test_link_is_correct(self):
        self.user = User.objects.create_user(username='teacher1', password='password123')
        self.client.login(username='teacher1', password='password123')

        response = self.client.get('/dashboard/teacher/')
        content = response.content.decode('utf-8')

        expected_link = '<link rel=\'stylesheet\' href=\'/static/bookings/css/teacherDashboard.css\'>'

        # Check if the expected link is in the response content
        if expected_link in content:
            print("DEBUG: Correct link found in HTML")
        else:
            print(f"DEBUG: Link NOT found. Expected {expected_link}")
            print("DEBUG: Content around link: ")
            print(content.split('<head>')[1].split('</head>')[0]) # print head section

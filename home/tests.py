from django.test import TestCase


class ToppageViewTests(TestCase):
    def test_logged_out_toppage(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "public.html")

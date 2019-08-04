from django.test import TestCase
from django.shortcuts import resolve_url

class ToppageViewTests(TestCase):
    def test_logged_out_toppage(self):
        response = self.client.get('/') # http://127.0.0.1:8000/
        self.assertEqual(response.status_code, 200) # hoge == hoge で判断、===ではなさそう
        self.assertContains(response, 'READ')

from unittest import TestCase
from app import app
from flask import Flask


class ForexTestCases(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_page_rendered(self):
        """Tests to make sure the page is rendered properly."""

        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)


    def test_conversion_success(self):
        """Tests to see if the conversion from one currency to another is successful."""

        res = self.client.post("/convert", data={"convert-from": "USD", "convert-to": "EUR", "amount": "100"})
        r = self.client.get("/")

        html = r.get_data(as_text=True)

        self.assertEqual(res.status_code, 302)
        self.assertIn("€82.01", html)


    def test_conversion_fail(self):
        """Tests to see if any invalid input is passed into the convert-from, convert-to, and amount fields. 
        Since the POST request returns a redirect to the home page with flash messages, this test ensures that the correct flash messages are displayed."""

        res = self.client.post("/convert", data={"convert-from": "currency", "convert-to": " another currency", "amount": ""})
        r = self.client.get("/")

        html = r.get_data(as_text=True)

        self.assertEqual(res.status_code, 302)
        self.assertIn("currency is not a valid currency.", html)
        self.assertIn("another currency is not a valid currency.", html)
        self.assertIn("Invalid amount entered.", html)

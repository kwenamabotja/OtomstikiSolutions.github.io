from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from main.models import Contact


class TestHomePage(TestCase):
    def setUp(self):
        self.email_test = "test@domain.test"

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        assert response.status_code == 200
        assert 'index.html' in [t.name for t in response.templates]
        assert 'base.html' in [t.name for t in response.templates]

    def test_home_page_contact_us(self):
        response = self.client.post(reverse('home'), data={
            "email": self.email_test,
            "name": self.email_test,
            "message": self.email_test,
        })
        assert response.status_code == 200
        assert 'index.html' in [t.name for t in response.templates]
        assert 'base.html' in [t.name for t in response.templates]
        c = Contact.objects.filter(email=self.email_test).first()
        assert c is not None
        assert c.name == self.email_test



from django.test import SimpleTestCase, TestCase

from authentication.models import User

# Create your tests here.
class test_newUser(TestCase):
    def setUp(self) :
        User.objects.create(email='testuser@gmail.com')
        
    def test_email(self):
        u = User.objects.get(email='testuser@gmail.com')
        self.assertEqual(u.email, 'testuser@gmail.com')
    def test_secend(self):
        pass

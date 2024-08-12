from django.test import TestCase
from .models import user

# Create your tests here.

class MyTestClass(TestCase):
      
    #create set up test
    def setUpTestData():
        # Set up non-modified objects used by all test methods
        user.objects.create(username = "test", password ="1234")

    #Test Username field
    def test_user_username(self):
        # Get a user object to test
        test = user.objects.get(id=1)

        # Get the metadata for the 'user' field and use it to query its data
        field_label = test._meta.get_field('username').verbose_name

        # Compare the value to the expected result
        self.assertEqual(field_label, 'username')
    
    #Test Username field length
    def test_username_max_length(self):
           # Get a user object to test
           test = user.objects.get(id=1)

           # Get the metadata for the 'username' field and use it to query its max_length
           max_length = test._meta.get_field('username').max_length

           # Compare the value to the expected result i.e. 120
           self.assertEqual(max_length, 20)

    #Test password field
    def test_user_password(self):
        # Get a user object to test
        test = user.objects.get(id=1)

        # Get the metadata for the 'password' field and use it to query its data
        field_label = test._meta.get_field('password').verbose_name

        # Compare the value to the expected result
        self.assertEqual(field_label, 'password')

    #Test password field length
    def test_user_password_max_length(self):
           # Get a user object to test
           test = user.objects.get(id=1)

           # Get the metadata for the 'password' field and use it to query its max_length
           max_length = test._meta.get_field('password').max_length

           # Compare the value to the expected result i.e. 120
           self.assertEqual(max_length, 20)
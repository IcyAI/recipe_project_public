from django.test import TestCase, Client
from .models import recipe
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import RecipesSearchForm, AddRecipeForm
from django.contrib.messages import get_messages

# Create your tests here.

class MyTestClass(TestCase):
      
    #create set up test
    def setUpTestData():
        # Set up non-modified objects used by all test methods
        recipe.objects.create(name = 'tea', cookingTime = 5, ingredients = ['water', 'tea leaves', 'sugar'])

    #Test name field
    def test_recipe_name(self):
        # Get a recipe object to test
        test = recipe.objects.get(id=1)

        # Get the metadata for the 'name' field and use it to query its data
        field_label = test._meta.get_field('name').verbose_name

        # Compare the value to the expected result
        self.assertEqual(field_label, 'name')
    
    #Test name field length
    def test_recipe_name_max_length(self):
           # Get a recipe object to test
           test = recipe.objects.get(id=1)

           # Get the metadata for the 'name' field and use it to query its max_length
           max_length = test._meta.get_field('name').max_length

           # Compare the value to the expected result i.e. 20
           self.assertEqual(max_length, 20)

    #Test cooking_time field
    def test_recipe_cooking_time(self):
        # Get a recipe object to test
        test = recipe.objects.get(id=1)

        # Get the metadata for the 'cookingTime' field and use it to query its data
        field_label = test._meta.get_field('cookingTime').verbose_name

        # Compare the value to the expected result
        self.assertEqual(field_label, 'cookingTime')

    #Test ingredients field
    def test_recipe_ingredients(self):
        # Get a recipe object to test
        test = recipe.objects.get(id=1)

        # Get the metadata for the 'ingredients' field and use it to query its data
        field_label = test._meta.get_field('ingredients').verbose_name

        # Compare the value to the expected result
        self.assertEqual(field_label, 'ingredients')

    #Test ingredients field length
    def test_recipe_ingredients_max_length(self):
           # Get a recipe object to test
           test = recipe.objects.get(id=1)

           # Get the metadata for the 'ingredients' field and use it to query its max_length
           max_length = test._meta.get_field('ingredients').max_length

           # Compare the value to the expected result i.e. 255
           self.assertEqual(max_length, 255)
    
    def test_get_absolute_url(self):
       test = recipe.objects.get(id=1)
       #get_absolute_url() should take you to the detail page of recipe #1
       #and load the URL /books/list/1
       self.assertEqual(test.get_absolute_url(), '/list/1')

# SEARCH
class RecipeFormTest(TestCase):
    def test_search_form_valid_data(self):
        # create a RecipesSearchForm instance with valid data
        form = RecipesSearchForm(
            data={
                "search_by": "name",
                "search_term": "Test Recipe",
                "cookingTime": "",
                "difficulty": "",
            }
        )

        # check if form is valid
        self.assertTrue(form.is_valid())

    def test_search_form_invalid_data(self):
        # create a RecipesSearchForm instance with empty data
        form = RecipesSearchForm(data={})

        # check if form is invalid
        self.assertFalse(form.is_valid())

    def test_search_form_field_labels(self):
        # create a RecipesSearchForm instance
        form = RecipesSearchForm()

        # check if "search_by" field label is "Search by"
        self.assertEqual(form.fields["search_by"].label, "Search by")

        # check if "search_term" field label is "Search term"
        self.assertEqual(form.fields["search_term"].label, "Search term")

        # check if "cooking_time" field label is "Cooking Time (minutes)"
        self.assertEqual(form.fields["cookingTime"].label, "Cooking Time in Minutes")

        # check if "difficulty" field label is "Difficulty"
        self.assertEqual(form.fields["difficulty"].label, "Difficulty")

class RecipeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create test user
        cls.user = User.objects.create_user(username="testuser", password="12345")

        # create test recipes
        cls.recipe1 = recipe.objects.create(
            name="Recipe 1", ingredients="ingredient1, ingredient2", cookingTime=10
        )
        cls.recipe2 = recipe.objects.create(
            name="Recipe 2", ingredients="ingredient1, ingredient2", cookingTime=20
        )

    def setUp(self):
        # initialize test client
        self.client = Client()

    def test_recipe_list_view_login_required(self):
        # send GET request to recipe list view
        response = self.client.get(reverse("recipes:list"))

        # check if response redirects to login page with the next parameter set to requested URL
        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('recipes:list')}"
        )

    def test_recipe_list_view(self):
        # log test user in
        self.client.login(username="testuser", password="12345")

        # send GET request to recipe list view
        response = self.client.get(reverse("recipes:list"))

        # check if response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # check if correct template is used
        self.assertTemplateUsed(response, "recipes/main.html")

        # check if response contains the first recipe name
        self.assertContains(response, "Recipe 1")

        # check if response contains the second recipe name
        self.assertContains(response, "Recipe 2")

    def test_recipe_detail_view_login_required(self):
        # send GET request to recipe detail view for the first recipe
        response = self.client.get(
            reverse("recipes:detail", kwargs={"pk": self.recipe1.pk})
        )

        # check if response redirects to login page with the next parameter set to requested URL
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('recipes:detail', kwargs={'pk': self.recipe1.pk})}",
        )

    def test_recipe_detail_view(self):
        # log test user in
        self.client.login(username="testuser", password="12345")

        # sends GET request to recipe detail view for the first recipe
        response = self.client.get(
            reverse("recipes:detail", kwargs={"pk": self.recipe1.pk})
        )

        # check if response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # check if correct template is used
        self.assertTemplateUsed(response, "recipes/detail.html")

        # check if response contains the first recipe name
        self.assertContains(response, "Recipe 1")

    def test_search_view_login_required(self):
        # send GET request to sort view
        response = self.client.get(reverse("recipes:sort"))

        # check if response redirects to login page with the next parameter set to requested URL
        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('recipes:sort')}"
        )

    def test_search_view(self):
        # log test user in
        self.client.login(username="testuser", password="12345")

        # send POST request to search view with valid data
        response = self.client.post(
            reverse("recipes:sort"),
            data={
                "search_by": "name",
                "search_term": "Recipe 1",
                "cooking_time": "",
                "difficulty": "",
            },
        )

        # check if response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # check if correct template is used
        self.assertTemplateUsed(response, "recipes/sort.html")

        # check if response contains the first recipe name
        self.assertContains(response, "Recipe 1")


class RecipeFormTest(TestCase):
    # test form validation with valid data
    def test_add_recipe_form_valid_data(self):
        form = AddRecipeForm(
            data={
                "name": "Test Recipe",
                "ingredients": "Test Ingredients",
                "cookingTime": 30,
                "pic": None,  # assuming no file for simplicity
            }
        )

        # form should be valid
        self.assertTrue(form.is_valid())

    # test form validation with no data
    def test_add_recipe_form_no_data(self):
        form = AddRecipeForm(data={})

        # form should be invalid
        self.assertFalse(form.is_valid())

        # should have errors for all required fields
        self.assertEqual(len(form.errors), 3)


class AddRecipeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create a test user
        cls.user = User.objects.create_user(username="testuser", password="12345")

    def setUp(self):
        # create a test client and log in the user
        self.client = Client()
        self.client.login(username="testuser", password="12345")

    # test GET request to addRecipe view
    def test_add_recipe_view_get(self):
        response = self.client.get(reverse("recipes:addRecipe"))

        # status code should be 200
        self.assertEqual(response.status_code, 200)

        # should use the correct template
        self.assertTemplateUsed(response, "recipes/addRecipe.html")

        # context should have AddRecipeForm
        self.assertIsInstance(response.context["add_recipe_form"], AddRecipeForm)

    # test POST request with valid data to addRecipe view
    def test_add_recipe_view_post_valid_data(self):
        data = {
            "name": "Test Recipe",
            "ingredients": "Test Ingredients",
            "cookingTime": 30,
            "pic": "",  # assuming no file for simplicity
        }

        response = self.client.post(reverse("recipes:addRecipe"), data)

        # should redirect after successful form submission
        self.assertEqual(response.status_code, 302)

        # should redirect to the recipe list view
        self.assertRedirects(response, reverse("recipes:list"))

        # one recipe should be created
        self.assertEqual(recipe.objects.count(), 1)

        # check for success message
        messages = list(get_messages(response.wsgi_request))

        # there should be one message
        self.assertEqual(len(messages), 1)

        # message content should be correct
        self.assertEqual(str(messages[0]), "Recipe added successfully")

    # test POST request with invalid data to addRecipe view
    def test_add_recipe_view_post_invalid_data(self):
        data = {}

        response = self.client.post(reverse("recipes:addRecipe"), data)

        # should return 200 status code
        self.assertEqual(response.status_code, 200)

        # should use the correct template
        self.assertTemplateUsed(response, "recipes/addRecipe.html")

        # form should be invalid
        self.assertFalse(response.context["add_recipe_form"].is_valid())

    # test that addRecipe view requires login
    def test_add_recipe_view_login_required(self):
        # log out the test user
        self.client.logout()

        response = self.client.get(reverse("recipes:addRecipe"))

        # should redirect to login page with next parameter set to addRecipe URL
        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('recipes:addRecipe')}"
        )
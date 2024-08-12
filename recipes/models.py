from django.db import models
from django.shortcuts import reverse

# Create your models here.

#recipe Model
class recipe(models.Model):

    #attributes
    name = models.CharField(max_length=20)
    cookingTime = models.IntegerField()
    ingredients = models.CharField( max_length= 255, help_text="Enter the ingredients, separated by a comma")
    difficulty = None
    pic = models.ImageField(upload_to='recipes', default='no_picture.jpg')

    # recipe difficulty
    @property
    def difficulty(self):
        ingredients = self.ingredients.split(", ")
        if self.cookingTime < 10 and len(ingredients) < 4:
            return "Easy"
        elif self.cookingTime < 10 and len(ingredients) >= 4:
            return "Medium"
        elif self.cookingTime >= 10 and len(ingredients) < 4:
            return "Intermediate"
        elif self.cookingTime >= 10 and len(ingredients) >= 4:
            return "Hard"
        return "Unknown"
    
    #print statement format
    def __str__(self):
        return "Name: {}, Cooking time: {} minutes, Ingredients: {}, Difficulty: {}".format(
            self.name,
            self.cookingTime,
            self.ingredients,
            self.difficulty or 'Not set'
        )
    
    #get url for recipe details
    def get_absolute_url(self):
       return reverse ('recipes:detail', kwargs={'pk': self.pk})
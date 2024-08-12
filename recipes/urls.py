from django.urls import path
#import views
from .views import home, sort, about, addRecipe
from .views import RecipeListView
from .views import RecipeDetailView

app_name = 'recipes' 

urlpatterns = [
   #home view
   path('', home, name= "home"),
   #Recipe List view
   path('list/', RecipeListView.as_view(), name='list'),
   #Recipe Details view
   path('list/<pk>', RecipeDetailView.as_view(), name='detail'),
   #sort recipe view
   path('sort/', sort, name = "sort"),
   #about me view
   path('about/',about, name="about"),
   #add recipe view
   path('addRecipe',addRecipe, name="addRecipe")
]

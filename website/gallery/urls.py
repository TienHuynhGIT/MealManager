from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('weekday_view/<str:day_of_week>', views.weekday_view, name='weekday_view'),
    path('create_recipe', views.create_recipe, name='create_recipe'),
    path('update_recipe/<int:id>', views.update_recipe, name='update_recipe'),
    path('add_recipe/<int:id>/<str:day_of_week>', views.add_recipe, name='add_recipe'),
    path('remove_recipe/<int:id>/<str:day_of_week>', views.remove_recipe, name='remove_recipe'),
    path('recipe_profile/<int:id>', views.recipe_profile, name='recipe_profile'),
    path('delete_recipe/<int:id>', views.delete_recipe, name='delete_recipe'),
]


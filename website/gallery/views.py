from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from . import models
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q


class RecipeForm(forms.ModelForm):
    class Meta:
        model = models.Recipe
        exclude = ['author', 'created_at', 'weekdays']


def home(request):
    context = {'monday': models.Recipe.objects.filter(entry__weekday__name='Montag', entry__user=request.user.id),
               'tuesday': models.Recipe.objects.filter(entry__weekday__name='Dienstag', entry__user=request.user.id),
               'wednesday': models.Recipe.objects.filter(entry__weekday__name='Mittwoch', entry__user=request.user.id),
               'thursday': models.Recipe.objects.filter(entry__weekday__name='Donnerstag', entry__user=request.user.id),
               'friday': models.Recipe.objects.filter(entry__weekday__name='Freitag', entry__user=request.user.id),
               'saturday': models.Recipe.objects.filter(entry__weekday__name='Samstag', entry__user=request.user.id),
               'sunday': models.Recipe.objects.filter(entry__weekday__name='Sonntag', entry__user=request.user.id)}
    return render(request, 'home.html', dict(context=context))


@login_required()
def weekday_view(request, day_of_week):
    user_filter = request.GET.get('filter')
    if user_filter == 'own':
        recipes = models.Recipe.objects.filter(author=request.user.id).all()
    else:
        recipes = models.Recipe.objects.filter(Q(author=request.user.id) | Q(published=True)).all()

    recipes_on_weekday = models.Recipe.objects.filter(entry__weekday__name=day_of_week, entry__user=request.user.id)
    context = {'recipes': recipes, 'recipes_on_weekday': recipes_on_weekday, 'day_of_week': day_of_week,
               'filter': user_filter}
    return render(request, 'weekday_view.html', dict(context=context))


@login_required()
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse('home'))
    else:
        form = RecipeForm()
    context = {'form': form, 'formtype': 'erstellen'}
    return render(request, 'recipe_form.html', dict(context=context))


@login_required()
def add_recipe(request, id, day_of_week):
    user_filter = request.GET.get('filter_reference')
    if user_filter == 'own':
        recipes = models.Recipe.objects.filter(author=request.user.id).all()
    else:
        recipes = models.Recipe.objects.filter(Q(author=request.user.id) | Q(published=True)).all()

    weekday = models.Weekday.objects.filter(name=day_of_week)

    if (day_of_week):
        entry = models.Entry(user=request.user, recepi=models.Recipe.objects.get(id=id), weekday=weekday.first())
        entry.save()

    recipes_on_weekday = models.Recipe.objects.filter(entry__weekday__name=day_of_week, entry__user=request.user.id)
    context = {'recipes': recipes, 'recipes_on_weekday': recipes_on_weekday, 'day_of_week': day_of_week,
               'filter': user_filter}
    return render(request, 'weekday_view.html', dict(context=context))


@login_required()
def remove_recipe(request, id, day_of_week):
    user_filter = request.GET.get('filter_reference_r')
    if user_filter == 'own':
        recipes = models.Recipe.objects.filter(author=request.user.id).all()
    else:
        recipes = models.Recipe.objects.filter(Q(author=request.user.id) | Q(published=True)).all()

    weekday = models.Weekday.objects.filter(name=day_of_week).first()

    entry = models.Entry.objects.filter(recepi=id, user=request.user.id, weekday=weekday).first()
    entry.delete()
    recipes_on_weekday = models.Recipe.objects.filter(entry__weekday__name=day_of_week, entry__user=request.user.id)
    context = {'recipes': recipes, 'recipes_on_weekday': recipes_on_weekday, 'day_of_week': day_of_week,
               'filter': user_filter}
    return render(request, 'weekday_view.html', dict(context=context))


def recipe_profile(request, id):
    recipe = models.Recipe.objects.get(id=id)
    return render(request, 'recipe_profile.html', dict(context=recipe))


@login_required()
def delete_recipe(request, id):
    recipe = models.Recipe.objects.get(id=id)
    if request.method == 'POST':
        recipe.delete()
        return HttpResponseRedirect(reverse('home'))
    return render(request, 'confirm.html', dict(context=recipe))


@login_required()
def update_recipe(request, id):
    recipe = models.Recipe.objects.get(id=id)
    form = RecipeForm(instance=recipe)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('home'))
        else:
            form = form
    recipe.delete()
    context = {'form': form, 'formtype': 'bearbeiten'}
    return render(request, 'recipe_form.html', dict(context=context))

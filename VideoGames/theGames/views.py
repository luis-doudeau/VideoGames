from django.shortcuts import render
from django.http import HttpResponse
from .models import Game, Studio
from django.http import Http404
from django.forms import ModelForm
from django.views import View  # Importez la classe View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView, UpdateView


def home(request):
    return HttpResponse('bonjour à tous')


def game_listing(request):
    games=Game.objects.all()
    return render(request, template_name='list_games.html', context={'games':games})

def game_detail(request, id):
    try :
     game=Game.objects.get(pk=id)
    except Game.DoesNotExist :
          raise Http404("Game does not exist")
    return render(request, template_name='game.html', context={'game':game})


class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ('name', 'description', 'studio')

    def clean(self):
        pass

def gameForm(request):
    gameForm = GameForm()
    # on teste si on est bien en validation du jeu (POST)
    if request.method == "POST":
        # Si oui on récupère les données postées
        form = GameForm(request.POST)
        # on vérifie la validité du jeu
        if form.is_valid():
            new_game = form.save()
            return redirect('game', id=new_game.id)
    # Si méthode GET, on présente le jeu
    context = {'form': gameForm}

    return render(request,'game_form.html', context)
    
class GameDeleteView(DeleteView):
    model = Game
    template_name = 'delete_game.html'
    success_url = reverse_lazy('games')

class GameEditView(UpdateView):
    model = Game
    fields = ['name', 'description', 'studio']
    template_name = 'edit_game.html'
    success_url = reverse_lazy('games')


class StudioForm(ModelForm):
    class Meta:
        model = Studio
        fields = ('name', 'description', 'country')

    def clean(self):
        pass

def studioForm(request):
    studioForm = StudioForm()
    # on teste si on est bien en validation du studio (POST)
    if request.method == "POST":
        # Si oui on récupère les données postées
        form = StudioForm(request.POST)
        # on vérifie la validité du studio
        if form.is_valid():
            new_studio = form.save()
            return redirect('studio', id=new_studio.id)
    # Si méthode GET, on présente le studio
    context = {'form': studioForm}

    return render(request,'studio_form.html', context)

def studio_listing(request):
    studios=Studio.objects.all()
    return render(request, template_name='list_studios.html', context={'studios':studios})

def studio_detail(request, id):
    try :
     studio=Studio.objects.get(pk=id)
    except Studio.DoesNotExist :
          raise Http404("Studio does not exist")
    return render(request, template_name='studio.html', context={'studio':studio})

class StudioDeleteView(DeleteView):
    model = Studio
    template_name = 'delete_studio.html'
    success_url = reverse_lazy('studios')

class StudioEditView(UpdateView):
    model = Studio
    fields = ['name', 'description', 'country']
    template_name = 'edit_studio.html'
    success_url = reverse_lazy('studios')


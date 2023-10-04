from django.shortcuts import render
from django.http import HttpResponse
from .models import Game
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
            context = {'game': new_game}
            return render(request,'game.html', context)
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
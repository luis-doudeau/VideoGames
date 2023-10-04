from django.shortcuts import render
from django.http import HttpResponse
from .models import Game
from django.http import Http404
from django.forms import ModelForm


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
    
class GameDelete(ModelForm):
    class Meta:
        model = Game
        fields = ('name', 'description', 'studio')

    def clean(self):
        pass

def my_task_delete(request):
    delete_game = get_object_or_404(Game, id=id)
    if request.method == "POST":
        delete_game.delete()
        # Rediriger vers la page de liste des jeux.
        return redirect('list_games')
    return render(request, 'delete_game.html', {'object': delete_game})
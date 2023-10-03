from django.shortcuts import render
from django.http import HttpResponse
from .models import Game


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


def gameForm(request):
    gameForm = TaskForm()
    # on teste si on est bien en validation de formulaire (POST)
    if request.method == "POST":
        # Si oui on récupère les données postées
        form = TaskForm(request.POST)
        # on vérifie la validité du formulaire
        if form.is_valid():
            new_game = form.save()
            context = {'game': new_game}
            return render(request,'game.html', context)
    # Si méthode GET, on présente le formulaire
    context = {'game': gameForm}

    return render(request,'game_form.html', context)
    

# def my_task_delete(request) :
#     taskform = TaskForm()
#     # on teste si on est bien en validation de formulaire (POST)
#     if request.method == "DELETE":
#         # Si oui on récupère les données postées
#         form = TaskForm(request.POST)
#         # on vérifie la validité du formulaire
#         if form.is_valid():
#             new_task = form.save()
#             context = {'task': new_task}
#             return render(request,'task.html', context)
#     # Si méthode GET, on présente le formulaire
#     context = {'form': taskform}

#     return render(request,'mytaskdelete.html', context)
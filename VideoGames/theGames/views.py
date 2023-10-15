from django.shortcuts import render
from django.http import HttpResponse
from .models import Game, Studio, Platform
from django.http import Http404
from django.forms import ModelForm
from django import forms
from django.views import View  # Importez la classe View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView


def home(request):
    return HttpResponse('bonjour à tous')


class GameListView(ListView):
    model = Game
    template_name = 'list_games.html'
    context_object_name = 'games'
    paginate_by = 5


class GameDetailView(DetailView):
    model = Game
    template_name = 'game.html'
    context_object_name = 'game'


class PlatformForm(forms.ModelForm):

    class Meta:
        model = Platform
        fields = ['name', 'description', 'manufacturer']


class GameForm(forms.ModelForm):
    studio = forms.ModelChoiceField(queryset=Studio.objects.all())
    nomPlatform = forms.CharField(
        required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    descriptionPlatform = forms.CharField(
        required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    manufacturerPlatform = forms.CharField(
        required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Game
        fields = ('name', 'description', 'studio', 'platforms')
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'}),
                   'description': forms.Textarea(attrs={'class': 'form-control'}),
                   'studio': forms.Select(attrs={'class': 'form-control'}),
                   'platforms': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})}

    def clean(self):
        pass


class GameCreateView(CreateView):
    model = Game
    form_class = GameForm
    template_name = 'game_form.html'
    success_url = reverse_lazy('games')

    def form_valid(self, form):
        # Vérification de l'existence d'un jeu avec le même nom
        if Game.objects.filter(name=form.cleaned_data['name']).exists():
            form.add_error('name', 'Un jeu avec ce nom existe déjà.')
            return self.form_invalid(form)

        # Tentative de création d'une nouvelle plateforme si des détails sont fournis
        new_platform = None
        if all(item in form.cleaned_data for item in ['nomPlatform', 'descriptionPlatform', 'manufacturerPlatform']):
            platform_name = form.cleaned_data['nomPlatform']

            # Vérification de l'existence d'une plateforme avec le même nom
            if not Platform.objects.filter(name=platform_name).exists():
                new_platform = Platform.objects.create(
                    name=platform_name,
                    description=form.cleaned_data['descriptionPlatform'],
                    manufacturer=form.cleaned_data['manufacturerPlatform']
                )
            else:
                form.add_error(
                    'nomPlatform', 'Une plateforme avec ce nom existe déjà.')
                return self.form_invalid(form)

        # Création du jeu
        game = form.save(commit=False)

        # Si une nouvelle plateforme a été créée, ajoutez-la aux plateformes associées au jeu
        if new_platform:
            game.save()  # Vous devez d'abord enregistrer le jeu avant de pouvoir modifier les relations ManyToMany
            game.platforms.add(new_platform)

        game.save()  # Sauvegarde des modifications finales

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['game_form'] = context.get('form')
        context['platform_form'] = context.get('form')
        return context


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


class StudioCreateView(CreateView):
    model = Studio
    form_class = StudioForm
    template_name = 'studio_form.html'
    success_url = reverse_lazy('studios')


class StudioListView(ListView):
    model = Studio
    template_name = 'list_studios.html'
    context_object_name = 'studios'


class StudioDetailView(DetailView):
    model = Studio
    template_name = 'studio.html'
    context_object_name = 'studio'


class StudioDeleteView(DeleteView):
    model = Studio
    template_name = 'delete_studio.html'
    success_url = reverse_lazy('studios')


class StudioEditView(UpdateView):
    model = Studio
    fields = ['name', 'description', 'country']
    template_name = 'edit_studio.html'
    success_url = reverse_lazy('studios')


class PlatformCreateView(CreateView):
    model = Platform
    fields = ['name', 'description', 'manufacturer']
    template_name = 'platform_form.html'
    success_url = reverse_lazy('create_game')

    def form_valid(self, form):
        if Platform.objects.filter(name=form.cleaned_data['name']).exists():
            form.add_error('name', 'Une plateforme avec ce nom existe déjà.')
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['platform_form'] = context.get('form')
        return context

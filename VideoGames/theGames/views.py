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
from fuzzywuzzy import process


class GameListView(ListView):
    model = Game
    template_name = 'list_games.html'
    context_object_name = 'games'
    paginate_by = 6


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
        # Si l'utilisateur a confirmé la création, effacez la nécessité de confirmation et continuez
        if 'confirm' in self.request.POST:
            # supprime 'confirmation_needed' s'il existe
            self.request.session.pop('confirmation_needed', None)
            # supprime 'error_message' s'il existe
            self.request.session.pop('error_message', None)
            return super().form_valid(form)

        # Si l'utilisateur a annulé, effacez la nécessité de confirmation et redirigez
        if 'cancel' in self.request.POST:
            # Nous préparons le même formulaire mais sans le besoin de confirmation
            context = self.get_context_data(form=form)
            # S'assurez qu'il n'y a pas de demande de confirmation
            context.pop('confirmation_needed', None)
            # S'assurez qu'il n'y a pas de message d'erreur
            context.pop('error_message', None)
            return self.render_to_response(context)

        game_name = form.cleaned_data['name']
        if Game.objects.filter(name__iexact=game_name.lower()).exists():
            form.add_error('name', 'Un jeu avec ce nom existe déjà.')
            return self.form_invalid(form)

        all_games = Game.objects.all()
        game_names = [
            game.name for game in all_games]
        # Récupère les 3 meilleurs résultats
        matches = process.extract(game_name, game_names, limit=3)

        for match, percent_similar in matches:
            if percent_similar > 80:
                # Mettre l'état de confirmation et le message d'erreur dans le contexte plutôt que dans la session
                context = self.get_context_data(form=form)
                context['confirmation_needed'] = True
                context['error_message'] = f"Un jeu avec un nom similaire '{match}' existe déjà avec {percent_similar}% de similarité. Veuillez confirmer que ce n'est pas une erreur."
                return self.render_to_response(context)

        existing_platforms_selected = form.cleaned_data.get(
            'platforms') and any(form.cleaned_data.get('platforms'))

        new_platform_name = form.cleaned_data.get('nomPlatform', '').strip()
        new_platform = None

        # Si aucune plateforme existante n'est sélectionnée, et que le nouveau nom de la plateforme est vide,
        # nous devons renvoyer une erreur.
        if not existing_platforms_selected and not new_platform_name:
            form.add_error(
                'nomPlatform', 'Le nom de la plateforme ne peut pas être vide')
            return self.form_invalid(form)

        # Si une nouvelle plateforme est spécifiée, vérifiez qu'elle n'existe pas déjà et créez-la si nécessaire
        if new_platform_name:  # cela signifie qu'il n'est pas vide
            if Platform.objects.filter(name=new_platform_name).exists():
                form.add_error(
                    'nomPlatform', 'Une plateforme avec ce nom existe déjà.')
                return self.form_invalid(form)

            new_platform = Platform.objects.create(
                name=new_platform_name,
                description=form.cleaned_data['descriptionPlatform'],
                manufacturer=form.cleaned_data['manufacturerPlatform']
            )

        game = form.save(commit=False)

        if new_platform:
            game.save()  # Enregistrement du jeu avant de pouvoir modifier les relations ManyToMany
            game.platforms.add(new_platform)

        game.save()

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
    form_class = GameForm
    template_name = 'edit_game.html'
    success_url = reverse_lazy('games')

    def form_valid(self, form):
        # Si l'utilisateur a confirmé la création, effacez la nécessité de confirmation et continuez
        if 'confirm' in self.request.POST:
            # supprime 'confirmation_needed' s'il existe
            self.request.session.pop('confirmation_needed', None)
            # supprime 'error_message' s'il existe
            self.request.session.pop('error_message', None)
            return super().form_valid(form)

        # Si l'utilisateur a annulé, effacez la nécessité de confirmation et redirigez
        if 'cancel' in self.request.POST:
            # Nous préparons le même formulaire mais sans le besoin de confirmation
            context = self.get_context_data(form=form)
            # Assurez-vous qu'il n'y a pas de demande de confirmation
            context.pop('confirmation_needed', None)
            # Assurez-vous qu'il n'y a pas de message d'erreur
            context.pop('error_message', None)
            return self.render_to_response(context)

        game_name = form.cleaned_data['name']
        if Game.objects.filter(name__iexact=game_name.lower()).exists() and Game.objects.get(pk=self.object.pk).name.lower() != game_name.lower():
            form.add_error('name', 'Un jeu avec ce nom existe déjà.')
            return self.form_invalid(form)

        nomGameNonChange = Game.objects.get(
            pk=self.object.pk).name == game_name

        if not nomGameNonChange:

            all_games = Game.objects.all()
            game_names = [
                game.name for game in all_games if game.name != Game.objects.get(pk=self.object.pk).name]
            # Récupère les 3 meilleurs résultats
            matches = process.extract(game_name, game_names, limit=3)

            for match, percent_similar in matches:
                print(percent_similar)
                if percent_similar > 80:
                    # Mettre l'état de confirmation et le message d'erreur dans le contexte plutôt que dans la session
                    context = self.get_context_data(form=form)
                    context['confirmation_needed'] = True
                    form.add_error('name', '')
                    context['error_message'] = f"Un jeu avec un nom similaire '{match}' existe déjà avec {percent_similar}% de similarité. Veuillez confirmer que ce n'est pas une erreur."
                    return self.render_to_response(context)

        existing_platforms_selected = form.cleaned_data.get(
            'platforms') and any(form.cleaned_data.get('platforms'))

        new_platform_name = form.cleaned_data.get(
            'nomPlatform', '').strip()
        new_platform = None

        # Si aucune plateforme existante n'est sélectionnée, et que le nouveau nom de la plateforme est vide,
        # nous devons renvoyer une erreur.
        if not existing_platforms_selected and not new_platform_name:
            form.add_error(
                'nomPlatform', 'Le nom de la plateforme ne peut pas être vide')
            return self.form_invalid(form)

        # Si une nouvelle plateforme est spécifiée, vérifiez qu'elle n'existe pas déjà et créez-la si nécessaire
        if new_platform_name:  # cela signifie qu'il n'est pas vide
            if Platform.objects.filter(name=new_platform_name).exists():
                form.add_error(
                    'nomPlatform', 'Une plateforme avec ce nom existe déjà.')
                return self.form_invalid(form)

            new_platform = Platform.objects.create(
                name=new_platform_name,
                description=form.cleaned_data['descriptionPlatform'],
                manufacturer=form.cleaned_data['manufacturerPlatform']
            )

        game = form.save(commit=False)

        if new_platform:
            game.save()  # Enregistrement du jeu avant de pouvoir modifier les relations ManyToMany
            game.platforms.add(new_platform)

        game.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['game_form'] = context.get('form')
        context['platform_form'] = context.get('form')
        return context


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

    def form_valid(self, form):
        if 'confirm' in self.request.POST:
            # supprime 'confirmation_needed' s'il existe
            self.request.session.pop('confirmation_needed', None)
            # supprime 'error_message' s'il existe
            self.request.session.pop('error_message', None)
            return super().form_valid(form)

        # Si l'utilisateur a annulé, effacez la nécessité de confirmation et redirigez
        if 'cancel' in self.request.POST:
            # Nous préparons le même formulaire mais sans le besoin de confirmation
            context = self.get_context_data(form=form)
            # Assurez-vous qu'il n'y a pas de demande de confirmation
            context.pop('confirmation_needed', None)
            # Assurez-vous qu'il n'y a pas de message d'erreur
            context.pop('error_message', None)
            return self.render_to_response(context)

        studio_name = form.cleaned_data['name']
        if Studio.objects.filter(name=studio_name).exists():
            form.add_error('name', 'Un studio avec ce nom existe déjà.')
            return self.form_invalid(form)

        all_studios = Studio.objects.all()
        studio_names = [studio.name for studio in all_studios]
        # Récupère les 3 meilleurs résultats
        matches = process.extract(studio_name, studio_names, limit=3)

        for match, percent_similar in matches:
            if percent_similar > 80:
                # Mettre l'état de confirmation et le message d'erreur dans le contexte plutôt que dans la session
                context = self.get_context_data(form=form)
                context['confirmation_needed'] = True
                form.add_error('name', '')
                context['error_message'] = f"Un studio avec un nom similaire '{match}' existe déjà avec {percent_similar}% de similarité. Veuillez confirmer que ce n'est pas une erreur."
                return self.render_to_response(context)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['studio_form'] = context.get('form')
        return context


class StudioListView(ListView):
    model = Studio
    template_name = 'list_studios.html'
    context_object_name = 'studios'
    paginate_by = 6


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
    form_class = StudioForm
    template_name = 'edit_studio.html'
    success_url = reverse_lazy('studios')

    def form_valid(self, form):
        if 'confirm' in self.request.POST:
            # supprime 'confirmation_needed' s'il existe
            self.request.session.pop('confirmation_needed', None)
            # supprime 'error_message' s'il existe
            self.request.session.pop('error_message', None)
            return super().form_valid(form)

        # Si l'utilisateur a annulé, effacez la nécessité de confirmation et redirigez
        if 'cancel' in self.request.POST:
            # Nous préparons le même formulaire mais sans le besoin de confirmation
            context = self.get_context_data(form=form)
            # Assurez-vous qu'il n'y a pas de demande de confirmation
            context.pop('confirmation_needed', None)
            # Assurez-vous qu'il n'y a pas de message d'erreur
            context.pop('error_message', None)
            return self.render_to_response(context)

        studio_name = form.cleaned_data['name']
        if Studio.objects.filter(name__iexact=studio_name.lower()).exists() and Studio.objects.get(pk=self.object.pk).name.lower() != studio_name.lower():
            form.add_error('name', 'Un studio avec ce nom existe déjà.')
            return self.form_invalid(form)

        nomStudioNonChange = Studio.objects.get(
            pk=self.object.pk).name == studio_name

        if not nomStudioNonChange:
            all_studios = Studio.objects.all()
            studio_names = [
                studio.name for studio in all_studios if studio.name != Studio.objects.get(pk=self.object.pk).name]
            # Récupère les 3 meilleurs résultats
            matches = process.extract(studio_name, studio_names, limit=3)

            for match, percent_similar in matches:
                if percent_similar > 80:
                    # Mettre l'état de confirmation et le message d'erreur dans le contexte plutôt que dans la session
                    context = self.get_context_data(form=form)
                    context['confirmation_needed'] = True
                    form.add_error('name', '')
                    context['error_message'] = f"Un studio avec un nom similaire '{match}' existe déjà avec {percent_similar}% de similarité. Veuillez confirmer que ce n'est pas une erreur."
                    return self.render_to_response(context)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['studio_form'] = context.get('form')
        return context


class PlatformCreateView(CreateView):
    model = Platform
    fields = ['name', 'description', 'manufacturer']
    template_name = 'platform_form.html'
    success_url = reverse_lazy('games')

    def form_valid(self, form):
        if Platform.objects.filter(name=form.cleaned_data['name']).exists():
            form.add_error('name', 'Une plateforme avec ce nom existe déjà.')
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['platform_form'] = context.get('form')
        return context

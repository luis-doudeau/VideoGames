from django.contrib import admin
from .models import Game, Studio, Platform


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    pass


@admin.register(Studio)
class GameAdmin(admin.ModelAdmin):
    pass


@admin.register(Platform)
class GameAdmin(admin.ModelAdmin):
    pass

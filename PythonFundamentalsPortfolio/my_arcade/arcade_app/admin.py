# arcade_app/admin.py

from django.contrib import admin
from .models import HighScore


@admin.register(HighScore)
class HighScoreAdmin(admin.ModelAdmin):
    list_display = ('player_name', 'game_name', 'score', 'achieved_at')
    list_filter = ('game_name',)
    search_fields = ('player_name', 'game_name')
    ordering = ('-score',)

# my_arcade/models.py

from django.db import models

"""
This module defines the HighScore model used to store
and display high score information for gameplay.
"""
class HighScore(models.Model):
    game_name = models.CharField(max_length=50)
    player_name = models.CharField(max_length=100, blank=True, null=True)
    score = models.IntegerField()
    achieved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score']  # Sort by highest score first

    def __str__(self):
        return f'{self.player_name or "Anonymous"} - {self.game_name} - {self.score}'

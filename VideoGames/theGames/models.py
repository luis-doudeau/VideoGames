from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateTimeField(auto_now_add=True)
    studio = models.CharField(max_length=200)

    def __str__(self):
        return self.name + self.description + str(self.release_date) + self.studio

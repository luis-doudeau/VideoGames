from django.db import models


class Studio(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=200)

    def __str__(self):
        return self.name + self.description + str(self.creation_date) + self.country

class Game(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateTimeField(auto_now_add=True)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + self.description + str(self.release_date) 

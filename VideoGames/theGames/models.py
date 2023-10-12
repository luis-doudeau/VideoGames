from django.db import models


class Studio(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Platform(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    manufacturer = models.CharField(max_length=100, help_text="The company that created the platform. e.g., Sony, Microsoft, Nintendo.")


    def __str__(self):
        return self.name 

class Game(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    release_date = models.DateTimeField(auto_now_add=True)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, related_name="games")
    platforms = models.ManyToManyField(Platform, related_name="games")


    def __str__(self):
        return self.name
    

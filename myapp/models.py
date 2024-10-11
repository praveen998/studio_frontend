from django.db import models

class Authentication(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=120)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
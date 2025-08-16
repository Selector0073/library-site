from django.db import models

class Users(models.Model):
    username = models.CharField(max_length=20)
    email = models.EmailField()
    passw = models.CharField(max_length=64)

    def __str__(self):
        return self.title
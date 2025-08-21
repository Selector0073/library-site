from django.db import models

class Login(models.Model):
    username = models.CharField('Username', max_length=20)
    email = models.EmailField('Email')
    passw = models.CharField('Password', max_length=128)
    expdate = models.DateField('Expand date')

    #def __str__(self):
        #return self.title
    
    class Meta:
        verbose_name = 'Login'
        verbose_name_plural = 'Logins'
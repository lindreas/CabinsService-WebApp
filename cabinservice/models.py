from django.db import models

class Orders(models.Model):
    date_of_service = models.DateField()
    cabin = models.CharField(max_length=200)
    service = models.CharField(max_length=200)

class Services(models.Model):
    type_of_service = models.CharField(max_length=200)
    def __str__(self):
        return self.type_of_service

class UserToken(models.Model):
    jwt_token = models.CharField(max_length=100)
    def __str__(self):
        return self.jwt_token

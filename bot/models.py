from django.db import models


class Profile(models.Model):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=125, null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=25, null=True, blank=True, default='user')
    def __str__(self):
        return f"{self.first_name}     {self.last_name}"


class Region(models.Model):
    name = models.CharField(max_length=125, null=True, blank=True)

    def __str__(self):
        return self.name

class Cargo(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True,blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    soni = models.PositiveIntegerField(null=True, blank=True, default=1)
    height = models.PositiveIntegerField(null=True, blank=True)
    width = models.PositiveIntegerField(null=True, blank=True)
    length = models.PositiveIntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=25, null=True, blank=True)
    status = models.CharField(max_length=125,null=True, blank=True, default="ko'rib chiqilmoqda")

    def __str__(self):
        return f"{self.user.first_name}     {self.name}     {self.status}"



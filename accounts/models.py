from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Series(models.Model):
	user_profile = models.CharField(max_length=100)
	seriesid = models.CharField(max_length=100)
	seriesname = models.CharField(max_length=100)
	vote_average = models.CharField(max_length=1000)

class SeriesForm(ModelForm):
	class Meta:
		model = Series
		fields = ['user_profile', 'seriesid']
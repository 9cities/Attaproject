from django.db import models
from django.contrib.auth.models import User


class Profil(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	security_question = models.CharField(max_length=200, blank=True)
	security_answer = models.CharField(max_length=200, blank=True)

	def __str__(self):
		return f"Profil: {self.user.username}"

# Create your models here.

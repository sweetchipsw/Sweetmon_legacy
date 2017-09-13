from django.db import models
from django.contrib.auth.models import User


class Issue(models.Model):
	owner = models.ForeignKey(User)

	title = models.CharField(max_length=200, blank=True, null=True)
	description = models.TextField(max_length=1024, blank=True, null=True)
	link = models.CharField(max_length=1024, blank=True, null=True)
	isopen = models.BooleanField(default=True)
	cve = models.CharField(max_length=200, blank=True, null=True)
	etc_numbering = models.CharField(max_length=200, blank=True, null=True)
	reward = models.IntegerField(default=0)

	def __str__(obj):
		return "%s" % (obj.title)

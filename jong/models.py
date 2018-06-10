# coding: utf-8
from django.db import models


class Rss(models.Model):

    """
        Rss
    """
    name = models.CharField(max_length=200, unique=True)
    status = models.BooleanField(default=False)
    notebook = models.CharField(max_length=200)
    url = models.URLField()
    tag = models.CharField(max_length=40, null=True, blank=True)
    date_triggered = models.DateTimeField(auto_now=True, auto_created=True)

    def show(self):
        """

        :return: string representing object
        """
        return "RSS %s %s" % (self.name, self.status)

    def __str__(self):
        return self.name

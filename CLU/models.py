from __future__ import unicode_literals

from django.db import models

class Build(models.Model):
    succes = (
        ('S', 'Sim'),
        ('N', 'Nao'),
    )
    buildCod = models.AutoField(primary_key=True)
    buildName = models.CharField(max_length=100)
    buildSucces = models.CharField(max_length=1, choices=succes)
    buildDate = models.DateTimeField('building date')


    def __str__(self):
        return self.buildName

class Branch(models.Model):

    default = (
        ('S', 'Sim'),
        ('N', 'Nao'),
    )

    branchCod       = models.AutoField(primary_key=True)
    branchName      = models.CharField(max_length=100)
    branchDefault   = models.CharField(max_length=1, choices=default)
    branchLastCommit = models.CharField(max_length=300)
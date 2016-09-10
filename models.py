# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Chat(models.Model):
    chatid = models.CharField(db_column='chatId', max_length=50)  # Field name made lowercase.
    title = models.CharField(max_length=140)
    type = models.CharField(max_length=10)
    username = models.CharField(db_column='userName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ignored = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chat'


class File(models.Model):
    fileid = models.CharField(db_column='fileId', max_length=255)  # Field name made lowercase.
    telegramtype = models.CharField(db_column='telegramType', max_length=100)  # Field name made lowercase.
    filetype = models.CharField(db_column='fileType', max_length=100)  # Field name made lowercase.
    filename = models.CharField(db_column='fileName', max_length=300)  # Field name made lowercase.
    md5 = models.CharField(max_length=300)

    class Meta:
        managed = False
        db_table = 'file'


class Message(models.Model):
    messageid = models.CharField(db_column='messageId', max_length=50)  # Field name made lowercase.
    text = models.TextField()
    date = models.DateTimeField()
    chatid = models.ForeignKey(Chat, models.DO_NOTHING, db_column='chatId', blank=True, null=True)  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId', blank=True, null=True)  # Field name made lowercase.
    pinned = models.IntegerField(blank=True, null=True)
    fileid = models.ForeignKey(File, models.DO_NOTHING, db_column='fileId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'message'


class User(models.Model):
    userid = models.CharField(db_column='userId', max_length=50)  # Field name made lowercase.
    firstname = models.CharField(db_column='firstName', max_length=50)  # Field name made lowercase.
    lastname = models.CharField(db_column='lastName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='userName', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user'

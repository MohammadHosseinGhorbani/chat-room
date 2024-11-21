from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    login_code = models.TextField("Login Code", max_length=5, null=True, blank=True)
    passed_login_code = models.BooleanField('Passed Login Code?', default=False)


class Room(models.Model):
    name = models.TextField(max_length=200)
    invite_link = models.TextField(max_length=36, unique=True)
    date_created = models.DateTimeField("date created")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_rooms")
    members_as_user = models.ManyToManyField(User, through='Member', related_name="joined_rooms")

    def __str__(self):
        return self.name


class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    join_date = models.DateTimeField("join date")
    is_admin = models.BooleanField()
    left = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'room')

    def __str__(self):
        return ("(!) " if self.is_admin else "") + self.user.username + " in " + self.room.name


class Message(models.Model):
    text = models.TextField(max_length=4000)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.ForeignKey(Member, on_delete=models.PROTECT)
    date = models.DateTimeField("date")
    replied_message = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return str(self.sender) + '(Message)'


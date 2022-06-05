from django.db import models
from django.contrib.auth.models import User


class Board2(models.Model):
    name1 = models.CharField(max_length=30, unique=True)
    description1 = models.CharField(max_length=100)

    def __str__(self):
        return self.name1


class Board(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    board2 = models.ForeignKey(Board2, on_delete=models.CASCADE, related_name='board_question', null=True, blank=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    subject = models.CharField(max_length=100)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question')
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='board_question', null=True, blank=True)
    photo = models.ImageField(null=True, upload_to="media/%Y/%m/%d", blank=True)

    def __str__(self):
        return self.subject


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')

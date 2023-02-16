import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models import User


class Course(models.Model):
    id = models.UUIDField(
        verbose_name=_("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(
        max_length=125,
        unique=True,
    )

    def __str__(self):
        return self.name


class Subject(models.Model):
    id = models.UUIDField(
        verbose_name=_("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    name = models.CharField(
        verbose_name=_("name"),
        max_length=127,
    )

    def __str__(self):
        return self.name


class Chapter(models.Model):
    id = models.UUIDField(
        verbose_name=_("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(
        max_length=125,
    )
    subject = models.ManyToManyField(Course)

    def __str__(self):
        return self.name


class Questions(models.Model):
    id = models.UUIDField(
        verbose_name=_("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.SET_NULL,
        null=True,
    )
    question = models.TextField()
    choice_1 = models.CharField(
        max_length=255,
    )
    choice_2 = models.CharField(
        max_length=255,
    )
    choice_3 = models.CharField(
        max_length=255,
    )
    choice_4 = models.CharField(
        max_length=255,
    )
    answer = models.CharField(
        max_length=255,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.question


class Exam(models.Model):
    id = models.UUIDField(
        verbose_name=_("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField(
        verbose_name=_("Exam Date"),
        auto_now_add=True,
    )
    is_completed = models.BooleanField(
        verbose_name=_("Complete Status"),
        default=False,
    )
    full_marks = models.IntegerField(
        verbose_name=_("Full Marks"),
    )
    obtained_marks = models.IntegerField(
        verbose_name=_("Obtained Marks"),
    )

    def __str__(self):
        return f"{self.user.name} - {self.course.name}"

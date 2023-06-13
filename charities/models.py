from django.db import models
from accounts.models import User


class Benefactor(models.Model):
    EXPERIENCE_CHOICES = (
        (0, 'Beginner'),
        (1, 'Intermediate'),
        (2, 'Expert'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experience = models.SmallIntegerField(choices=EXPERIENCE_CHOICES, default=0)
    free_time_per_week = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.user


class Charity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    reg_number = models.CharField(max_length=10)

    def __str__(self):
        return self.user



class TaskManager(models.Manager):
    def related_tasks_to_charity(self, user):
        return self.filter(charity=user)

    def related_tasks_to_benefactor(self, user):
        return self.filter(benefactor=user)

    def all_related_tasks_to_user(self, user):
        return self.filter(models.Q(benefactor=user) | models.Q(charity=user) | models.Q(status='Pending'))


class Task(models.Model):
    STATE_CHOICES = (
        ('P', 'Pending'),
        ('W', 'Waiting'),
        ('A', 'Assigned'),
        ('D', 'Done'),
    )
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    assigned_benefactor = models.ForeignKey('Benefactor', on_delete=models.SET_NULL, null=True, blank=True)
    charity = models.ForeignKey('Charity', on_delete=models.CASCADE)
    age_limit_from = models.IntegerField(null=True, blank=True)
    age_limit_to = models.IntegerField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    gender_limit = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    state = models.CharField(max_length=1, choices=STATE_CHOICES, default='P')
    title = models.CharField(max_length=60)

    def __str__(self):
        return self.title

    objects = TaskManager()
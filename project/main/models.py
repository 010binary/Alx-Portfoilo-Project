from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255, verbose_name=_('name'))
    username = models.CharField(
        max_length=255, unique=True, null=False, blank=False, verbose_name=_('username'))
    mobile_no = models.CharField(
        max_length=20, unique=True, null=False, blank=False, verbose_name=_('mobile_no'))
    email = models.EmailField(unique=True, null=False,
                              blank=False, verbose_name=_('email'))
    password = models.CharField(max_length=500)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['name', 'username', 'mobile_no']

    objects = UserManager()

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super().save(*args, **kwargs)


class Competition(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=False, blank=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=(
        ('Active', 'Active'), ('Inactive', 'Inactive')))

    def __str__(self):
        return self.name


class Candidate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=False, blank=False)
    competition = models.ForeignKey(
        Competition, related_name="candidates", on_delete=models.CASCADE)
    total_votes = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(
        Competition, related_name="votes", on_delete=models.CASCADE)
    candidate = models.ForeignKey(
        Candidate, related_name="votes", on_delete=models.CASCADE)
    vote_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()

    class Meta:
        # Enforce one vote per user per competition
        unique_together = ('user', 'competition')

    def __str__(self):
        return f"Vote by {self.user.username} for {self.candidate.name} in {self.competition.name}"

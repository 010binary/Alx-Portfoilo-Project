from django.contrib import admin
from .models import User, Candidate, Competition, Vote

# Register your models here.
admin.site.register(User)
admin.site.register(Candidate)
admin.site.register(Competition)
admin.site.register(Vote)